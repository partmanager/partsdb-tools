from .BoxPackaging import BoxPackaging
from .BulkBoxPackaging import BulkBoxPackaging
from .TapeBoxPackaging import TapeBoxPackaging
from .TapeReelPackaging import TapeReelPackaging
from .Box import box_from_dict
from .Reel import reel_from_dict
from .Tape import tape_from_dict

def decode_box(packaging_dict):
    code = packaging_dict['code']
    qty = packaging_dict['qty']
    box = None
    if 'packagingData' in packaging_dict:
        if 'box' in packaging_dict['packagingData']:
            box = box_from_dict(packaging_dict['packagingData']['box'])
    return BoxPackaging(code, qty, box)


def decode_bulk_box(packaging_dict):
    code = packaging_dict['code']
    qty = packaging_dict['qty']
    box = None
    if 'packagingData' in packaging_dict:
        if 'box' in packaging_dict['packagingData']:
            box = box_from_dict(packaging_dict['packagingData']['box'])
    return BulkBoxPackaging(code, qty, box)


def decode_tape_box(packaging_dict):
    code = packaging_dict['code']
    qty = packaging_dict['qty']
    return TapeBoxPackaging(code, qty, None)


def decode_tape_reel(packaging_dict):
    code = packaging_dict['code']
    qty = packaging_dict['qty']
    packaging = TapeReelPackaging(code, qty, reel=None, tape=None)
    if 'packagingData' in packaging_dict:
        if 'reel' in packaging_dict['packagingData']:
            packaging.reel = reel_from_dict(packaging_dict['packagingData']['reel'])
        if 'tape' in packaging_dict['packagingData']:
            packaging.tape = tape_from_dict(packaging_dict['packagingData']['tape'])
    return packaging



packaging_map = {
    'Box': decode_box,
    'Bulk/Box': decode_bulk_box,
    'Tape/Box': decode_tape_box,
    'Tape/Reel': decode_tape_reel
}

def packaging_from_dict(packaging_dict):
    if 'type' in packaging_dict:
        packaging_type = packaging_dict['type']
        if packaging_type in packaging_map:
            return packaging_map[packaging_type](packaging_dict)
    return None