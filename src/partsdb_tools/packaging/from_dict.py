from .TapeReelPackaging import TapeReelPackaging
from .Reel import reel_from_dict
from .Tape import tape_from_dict


def decode_tape_reel(packaging_dict):
    tape, reel = packaging_dict['type'].split('/')
    code = packaging_dict['code']
    qty = packaging_dict['qty']
    packaging = TapeReelPackaging(code, qty, reel=None, tape=None)
    if 'packagingData' in packaging_dict:
        if 'reel' in packaging_dict['packagingData']:
            packaging.reel = reel_from_dict(packaging_dict['packagingData']['reel'])
        if 'tape' in packaging_dict['packagingData']:
            packaging.tape = tape_from_dict(packaging_dict['packagingData']['tape'])

packaging_map = {
    'Paper Tape/Reel': decode_tape_reel
}

def packaging_from_dict(packaging_dict):
    if 'type' in packaging_dict:
        packaging_type = packaging_dict['type']
        if packaging_type in packaging_map:
            return packaging_map[packaging_type](packaging_dict)
    return None