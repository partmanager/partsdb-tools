import argparse
import rawpy
import cv2 as cv
import numpy as np

from pathlib import Path
from .detail.outputImageParameters import OutputImageParameters
from .detail.boundingBox import BoundingBox
from .detail.file_operations import load_json
from .components.Part import part_from_dict


min_size_x = 640*2
min_size_y = 480*2
small_object_size_x=640*2
small_object_size_y=480*2

def main():
    parser = argparse.ArgumentParser(description="Picture tool")
    parser.add_argument('-b', '--background_image', type=Path, help="Background image")
    parser.add_argument('-i', '--input_dir', type=Path, help="Input image directory")
    parser.add_argument('-o', '--output_dir', type=Path, help="Output image directory")
    parser.add_argument('-d', '--debug', action='store_true', help="Enable debug mode")
    parser.add_argument('-p', '--product_file', type=Path, help="""Path to *.json product description file.
    When provided, output images will be stored in 'pictures' directory placed in the same place as product description file.
    Input images will be read from 'RAW/pictures' directory placed in the same place as product description file.
    Product pictures are expected to be placed inside 'RAW/pictures/product/,
    packaging pictures should be placed in 'RAW/pictures/packaging'""")
    parser.add_argument('--output_image_size_x', type=int, default=640, help="Output image size")
    parser.add_argument('--output_image_size_y', type=int, default=480, help="Output image size")
    args = parser.parse_args()

    out_img_params = OutputImageParameters(args.output_image_size_x, args.output_image_size_y, 20)

    if args.product_file is not None:
        process_product_images(args, out_img_params)
    else:
        image_collections = load_images(args.input_dir, args.background_image)
        for collection in image_collections:
            try:
                print("Processing", collection)
                processed_images = process_images(
                    image_collections[collection]["background"],
                    image_collections[collection]["images"],
                    out_img_params,
                    debug=args.debug
                )
                for processed_image_name in processed_images:
                    save_images(processed_images[processed_image_name], args.output_dir, processed_image_name, manufacturers)
            except Exception as e:
                print(f"Exception while processing {collection}: ", e)


def process_product_images(args, out_img_params: OutputImageParameters):
    product_json = load_json(args.product_file)
    part = part_from_dict(product_json)
    product_images_dir = args.product_file.parent.joinpath('RAW', 'pictures', 'product')
    picture_dest_dir = args.product_file.parent.joinpath('pictures')
    picture_prefix = f"{part.manufacturer}__{part.part_number}__".replace(' ', '_')

    print(f"""
Processing pictures for {part.part_number}
    Working directory: {args.product_file.parent}
    Processed images will be placed in {picture_dest_dir}
    Images will have prefix: {picture_prefix}
""")

    images, collection = load_images(product_images_dir, None)
    processed_images = process_images(None, images, out_img_params)
    save_images(picture_dest_dir, processed_images, picture_prefix)


def process_images(background, images, out_image_params: OutputImageParameters, debug=False):
    images_grayscale = []
    for bgr_img in images:
        images_grayscale.append(cv.cvtColor(bgr_img, cv.COLOR_BGR2GRAY))
    final_bounding_box = find_bounding_box(images_grayscale, background, out_image_params, debug)

    processed_images = []
    for img in images:
        cropped_image = crop_image(img, final_bounding_box)
        resized_image = resize_image(cropped_image, out_image_params)
        processed_images.append(resized_image)

    return processed_images


def find_common_bounding_box(images, background, debug):
    back_sub = cv.createBackgroundSubtractorMOG2(history=10, varThreshold=200, detectShadows=False)
    for i in range(4):
        back_sub.apply(background)

    fg_masks = []
    for image_name in images:
        fg_masks.append(back_sub.apply(images[image_name]))
        if debug:
            cv.imshow('FG Mask', cv.resize(fg_masks[-1], (640, 480), interpolation=cv.INTER_AREA))
            cv.waitKey(300)

    fg_mask = cv.bitwise_or(filterout_small_elements(fg_masks[-2]), filterout_small_elements(fg_masks[-1]))
    if debug:
        cv.imshow('FG Mask sum', cv.resize(fg_mask, (640, 480), interpolation=cv.INTER_AREA))
        cv.waitKey(300)
    return  get_bounding_box(fg_mask)

def find_common_bounding_box_v2(images, background, debug):
    back_sub = cv.createBackgroundSubtractorKNN()
    fg_mask = None
    for i in range(len(images)):
        fg_mask = back_sub.apply(images[i])

    se2 = cv.getStructuringElement(cv.MORPH_RECT, (20,20))
    fg_mask = cv.morphologyEx(fg_mask, cv.MORPH_OPEN, se2)

    cnts, hierarchy = cv.findContours(fg_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    area = 0
    index = None
    for i, contur in enumerate(cnts):
        if cv.contourArea(contur) > area:
            area = cv.contourArea(contur)
            index = i

    x, y, w, h = cv.boundingRect(cnts[index])
    return BoundingBox(x, x+w, y, y+h), fg_mask


def find_bounding_box(images, background, out_image_params: OutputImageParameters, debug):
    bounding_box, gf_mask = find_common_bounding_box_v2(images, background, debug)

    if is_small_object(bounding_box):
        dims = inside_min_image(bounding_box)
        x1, x2, y1, y2 = dims
        final_bounding_box = BoundingBox(x1 - out_image_params.border,
                                         x2 + out_image_params.border,
                                         y1 - out_image_params.border,
                                         y2 + out_image_params.border)
    else:
        final_bounding_box = bounding_box_to_proportion(
            bounding_box,
            images[0].shape[1],
            images[0].shape[0],
            out_image_params)
    return final_bounding_box


def resize_image(image, out_image_params: OutputImageParameters):
    return cv.resize(
        image,
        (out_image_params.width, out_image_params.height),
        interpolation=cv.INTER_AREA
    )


def load_images(input_dir: Path, background_image: Path):
    image_collection = {}
    images = []
    images_gray = []
    for file in input_dir.glob('**/*'):
        if file.is_file():
            if file.suffix in ['.CR2']:
                raw = rawpy.imread(str(file.resolve()))
                rgb = raw.postprocess()
                bgr = cv.cvtColor(rgb, cv.COLOR_RGB2BGR)
                images.append(bgr)
            else:
                bgr_image = cv.imread(str(file.resolve()))
                images.append(bgr_image)

    if background_image is not None and background_image.is_file():
        background_img = cv.imread(background_image.resolve())
        for collection in image_collection:
            if image_collection[collection]["background"] is None:
                image_collection[collection]["background"] = background_img
    return images, image_collection


def save_images(output_dir: Path, images, prefix):
    for i, image in enumerate(images, start=1):
        write_path = output_dir.joinpath(prefix + str(i)).with_suffix(".jpg")
        write_path.parent.mkdir(parents=True, exist_ok=True)
        status = cv.imwrite(str(write_path.resolve()), image)
        if not status:
            print("Error writing image:", write_path.resolve())


def is_small_object(bounding_box):
    if bounding_box.size_x <= small_object_size_x and bounding_box.size_y <= small_object_size_y:
        return True
    else:
        return False


def filterout_small_elements(fg_mask):
    nb_blobs, im_with_separated_blobs, stats, _ = cv.connectedComponentsWithStats(fg_mask)
    sizes = stats[:, cv.CC_STAT_AREA]
    min_size = 1000

    im_result = np.zeros_like(im_with_separated_blobs, dtype=np.uint8)
    for index_blob in range(1, nb_blobs):
        if sizes[index_blob] >= min_size:
            im_result[im_with_separated_blobs == index_blob] = 255
    return im_result


def bounding_box_to_proportion(bounding_box, image_width, image_height, image_parameters: OutputImageParameters):
    if bounding_box.ratio > image_parameters.ratio:
        # add borders and adjust heigh
        scaling_ratio = bounding_box.size_x / image_parameters.object_width
        width_border = image_parameters.border * scaling_ratio
        if bounding_box.xmin - width_border < 0:
            width_border = bounding_box.xmin
            scaling_ratio = (bounding_box.size_x + 2*width_border) / image_parameters.width
        height = image_parameters.height * scaling_ratio
        if height > image_height:
            if image_width / image_height == image_parameters.ratio:
                return BoundingBox(0, image_width, 0, image_height)
            else:
                print(f"Original image ratio {image_width/image_height}, "
                      f"requested ratio {image_parameters.ratio}, scaling factor: {scaling_ratio}, scaled height: {height}")
                raise ValueError("Unable to fit bounding box with requested image ratio")
        center_y = bounding_box.center()[1]
        y_min = int(center_y - height / 2)
        return BoundingBox(int(bounding_box.xmin - width_border),
                           int(bounding_box.xmax + width_border),
                           y_min,
                           int(y_min + height)
        )
    else:
        print("Adjusting width")
        # add borders and adjust width
        scaling_ratio = bounding_box.size_y / image_parameters.object_height
        height_border = image_parameters.border * scaling_ratio
        if bounding_box.ymin - height_border < 0:
            height_border = bounding_box.ymin
            scaling_ratio = (bounding_box.size_y + 2*height_border) / image_parameters.height
        width_border = image_parameters.border * scaling_ratio

    return BoundingBox(int(bounding_box.xmin - width_border),
                       int(bounding_box.xmax + width_border),
                       int(bounding_box.ymin * scaling_ratio - height_border),
                       int(bounding_box.ymax * scaling_ratio + height_border)
    )


def get_bounding_box(elements):
    pts = np.argwhere(elements>0)
    y1, x1 = pts.min(axis=0)
    y2, x2 = pts.max(axis=0)
    return BoundingBox(x1, x2, y1, y2, elements.shape[1], elements.shape[0])


def crop_image(image, bounding_box):
    return image[
           bounding_box.ymin:bounding_box.ymax,
           bounding_box.xmin:bounding_box.xmax]


def inside_min_image(bounding_box):
    if bounding_box.size_x <= min_size_x and bounding_box.size_y <= min_size_y:
        middle_x = int(bounding_box.xmin + bounding_box.size_x / 2)
        middle_y = int(bounding_box.ymin + bounding_box.size_y / 2)
        return middle_x - min_size_x, middle_x + min_size_x, middle_y - min_size_y, middle_y + min_size_y
    return None
