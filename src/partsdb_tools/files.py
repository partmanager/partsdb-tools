import argparse
import shutil
import json

from pathlib import Path
import urllib.request
from urllib.parse import urlparse, unquote

from .common import load_files
from .components.File import FileVersion
from .components.Part import Part, part_from_dict
from .detail.file_operations import load_json, find_file_by_md5sum, calculate_md5


class FileData:
    def __init__(self, filename, url, manufacturer, filetype, revision, date, md5sum, path):
        self.filename = Path(filename if filename is not None else self.filename_from_url(url))
        self.url = url
        self.manufacturer = manufacturer
        self.filetype = filetype
        self.revision = revision
        self.date = date
        self.md5sum = md5sum
        self.path = path

    def set_destination_directory(self, destination_directory):
        manufacturer = self.manufacturer.replace(" ", "_").lower()
        file_name = f"{manufacturer}__{self.filename.stem}__{self.md5sum}"
        self.path = destination_directory.joinpath(manufacturer, file_name).with_suffix(self.filename.suffix)

    def exists(self):
        return self.path.exists() and self.path.is_file()

    def validate(self):
        return self.md5sum == calculate_md5(self.path)

    def download(self):
        local_filename, headers = urllib.request.urlretrieve(self.url)
        md5sum = calculate_md5(local_filename)
        if md5sum == self.md5sum:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(local_filename, self.path)

    def filename_from_url(self, url):
        return Path(unquote(urlparse(url).path).replace(' ', '_')).name


def main():
    parser = argparse.ArgumentParser(description="Part DB tools")
    parser.add_argument('-i', '--input', type=Path, help="Path to the input file (*.json)")
    parser.add_argument('-a', '--add', type=Path, help="Add attachment file into part *.json file")
    parser.add_argument('-d', '--directory', help="Path to the input directory")
    parser.add_argument('-o', '--output', type=Path, help="Path to the output directory")
    parser.add_argument('-v', '--validate_only', action='store_true', help="Validate files")
    parser.add_argument('--info', type=Path, help="Show file information")
    args = parser.parse_args()

    if args.input:
        input_files = [args.input]
    elif args.directory:
        input_files = load_files(args.directory)
    elif args.info:
        show_file_info(args.info)
        exit(1)
    else:
        print("No input or directory specified")
        exit(-1)

    process_attachment_files(input_files, args.output)


def show_file_info(filepath: Path):
    if not filepath.is_file():
        print("Provided path don't point to a file.")
        return
    file_version = FileVersion(None, filepath)
    file_version.set_md5()
    file_version.read_metadata()
    file_version.process_metadata()
    file_dict = {
        "type": "Unknown",
        "versions": {
            file_version.revision: file_version.to_dict()
        }
    }
    print(json.dumps(file_dict, indent='\t'))


def process_attachment_files(parts_files, output_path: Path, download_missing = False):
    for part_file in parts_files:
        parts = [part_from_dict(load_json(part_file), part_file)]
        for part in parts:
            process_part_attachment_files(part, output_path, download_missing)


def process_part_attachment_files(part: Part, output_path: Path, download_missing = False):
            for file in part.files:
                file_extension = Path(file.filename).suffix[1:]
                if not file.versions_supported:
                    print("Skipping file, versions not supported")
                else:
                    for key, version in file.versions.items():
                        destination = output_path.joinpath(version.filename(part.manufacturer, part.part_number, file_extension))
                        destination.parent.mkdir(parents=True, exist_ok=True)
                        version.filepath = destination
                        if destination.exists():
                            print("file already exists, validating")
                            if not version.validate():
                                print("file validation failed")
                        else:
                            print(f"File missing: {destination}")
                            print("Checking RAW directory for missing file.")
                            files_dir = Path(part.file_location.parent).joinpath('RAW', 'documents')
                            print(files_dir)
                            found = find_file_by_md5sum(files_dir, version.md5sum)
                            if found:
                                print("Found file", found, "renaming and moving into destination directory")
                                shutil.copyfile(found[0], destination)
                            elif download_missing:
                                print("Downloading")
                                f.download()


def copy_and_rename_file(input_file: Path, output_dir: Path):
    manufacturer = input_file.stem.split("__")[0]
    file_name = input_file.stem.split("__")[1]
    md5_sum = calculate_md5(input_file)

    new_filename = f"{manufacturer}__{file_name}__{md5_sum}.{input_file.suffix}"
    new_file_path = output_dir.joinpath(new_filename)

    shutil.copyfile(input_file.resolve(), new_file_path.resolve())