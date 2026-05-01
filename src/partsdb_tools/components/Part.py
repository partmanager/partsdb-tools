from .OrderNumber import order_number_from_dict
from .Series import series_from_dict


class Part:
    def __init__(self, part_type, manufacturer, part_number):
        self.part_type = part_type
        self.manufacturer = manufacturer
        self.part_number = part_number
        self.marking_code = None
        self.series = []
        self.description = None
        self.product_URL = None
        self.notes = None
        self.tags = set()
        self.storage_conditions = None
        self.operating_conditions = None
        self.parameters = {}
        self.files = {}
        self.package = None
        self.symbol = None
        self.footprint = None
        self.order_numbers: dict = {}

    def add_order_number(self, order_number, force=False):
        if order_number.order_number in self.order_numbers and not force:
            raise ValueError('Already in order numbers')
        self.order_numbers[order_number.order_number] = order_number

    def add_series(self, series):
        self.series.append(series)

    def merge(self, part):
        if self.compare(part) == 0:
            self.order_numbers.update(part.order_numbers)

    def compare(self, part):
        if (self.part_number != part.part_number or
                self.manufacturer != part.manufacturer or
                self.part_type != part.part_type):
            return -1
        return 0

    def to_dict(self):
        result = {
            'manufacturer': self.manufacturer,
            'partNumber': self.part_number,
            'partType': self.part_type,
            'storageConditions': self.storage_conditions,
            'operatingConditions': self.operating_conditions
        }
        if self.marking_code:
            result['markingCode'] = self.marking_code
        if self.series:
            tmp = []
            for series in self.series:
                tmp.append(series.to_dict())
            result['series'] = tmp
        if self.description:
            result['description'] = self.description
        if self.product_URL:
            result['productUrl'] = self.product_URL
        if self.notes:
            result['notes'] = self.notes
        if self.tags:
            result['tags'] = self.tags
        if self.parameters:
            result['parameters'] = self.parameters
        if self.files:
            result['files'] = self.files
        if self.package:
            result['package'] = self.package.to_dict()
        if self.symbol:
            result['symbol&footprint'] = self.symbol
        # if self.footprint:
        #     result['footprint'] = self.footprint
        if self.order_numbers:
            result['orderNumbers'] = {}
            for k, order in self.order_numbers.items():
                result['orderNumbers'][k] = order.to_dict()

        return result

    def validate(self):
        if not self.validate_part_type():
            return False
        if len(self.manufacturer) == 0:
            return False
        if len(self.part_number) == 0:
            return False
        return True

    def validate_part_type(self):
        return self.part_type in []


def part_from_dict(part_dict) -> Part:
    part = Part(part_dict['partType'], part_dict['manufacturer'], part_dict['partNumber'])
    if 'storageConditions' in part_dict:
        part.storage_conditions = part_dict['storageConditions']
    if 'operatingConditions' in part_dict:
        part.storage_conditions = part_dict['operatingConditions']
    if 'markingCode' in part_dict:
        part.marking_code = part_dict['markingCode']
    if 'series' in part_dict:
        for series_dict in part_dict['series']:
            part.series.append(series_from_dict(series_dict, part.manufacturer))
    if 'description' in part_dict:
        part.description = part_dict['description']
    if 'productUrl' in part_dict:
        part.product_URL = part_dict['productUrl']
    if 'notes' in part_dict:
        part.notes = part_dict['notes']
    if 'tags' in part_dict:
        part.tags = part_dict['tags']
    if 'parameters' in part_dict:
        part.parameters = part_dict['parameters']
    if 'files' in part_dict:
        part.files = part_dict['files']
    if 'package' in part_dict:
        part.package = part_dict['package']
    if 'symbol&footprint' in part_dict:
        part.symbol = part_dict['symbol&footprint']
    if 'orderNumbers' in part_dict:
        part.order_numbers = {}
        for k, order_dict in part_dict['orderNumbers'].items():
            assert k not in part.order_numbers
            part.order_numbers[k] = order_number_from_dict(k, order_dict)
    return part
