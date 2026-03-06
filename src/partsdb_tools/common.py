import json
from pathlib import Path
from .config.PartTypes import part_types


def load_part_types():
    part_types_dict = {}
    for item in part_types.keys():
        required_fields = part_types[item]['required_fields'] if 'required_fields' in part_types[item] else []
        required_parameters = part_types[item]['required_parameters'] if 'required_parameters' in part_types[item] else []
        part_types_dict[item] = {
            'required_fields': required_fields,
            'required_parameters': required_parameters
        }
        if 'subcategory' in part_types[item] and len(part_types[item]['subcategory']) > 0:
            for subitem_key in part_types[item]['subcategory']:
                subitem = part_types[item]['subcategory'][subitem_key]
                part_types_dict[subitem_key] = {
                    'required_fields': required_fields + subitem['required_fields'] if 'required_fields' in subitem else [],
                    'required_parameters': required_parameters +  subitem['required_parameters'] if 'required_parameters' in subitem else []
                }
    return set(part_types_dict.keys()), part_types_dict


def load_manufacturers(path: Path):
    with open(path) as f:
        manufacturers = json.load(f)
        return [x['name'] for x in manufacturers] + [x['full_name'] for x in manufacturers if
                                                     x['full_name'] is not None and len(x['full_name']) > 0]


def load_packaging_types():
    return ['Bag', 'Bulk', 'Cut Tape', 'Embossed Tape / Reel', 'Paper Tape / Reel', 'Foil',
            'shrink wrap', 'Tube', 'Tray', '', 'Tape & Reel', '13” Reel', '7" reel', 'Tape/Reel']


def load_msl_classification():
    return ['MSL-1 UNLIM',
            'MSL-2 1-YEAR',
            'MSL-2A 4-WEEKS',
            'MSL-3 168-HOURS',
            'MSL-4 72-HOURS',
            'MSL-5 48-HOURS',
            'MSL-5A 24-HOURS',
            'MSL-6 TOL']


def load_files(directory):
    files = Path(directory).rglob('*.json')
    return [x for x in files if not str(x).endswith('_generated.json')]
