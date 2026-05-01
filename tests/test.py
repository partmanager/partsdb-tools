import unittest
from src.partsdb_tools.components.Part import Part, part_from_dict
from src.partsdb_tools.components.OrderNumber import OrderNumber
from src.partsdb_tools.components.Series import Series
from src.partsdb_tools.packaging.TapeReelPackaging import TapeReelPackaging
from src.partsdb_tools.packaging.Tape import Tape
from src.partsdb_tools.packaging.Reel import Reel
from src.partsdb_tools.units.Value import Value as Dim


class Test(unittest.TestCase):
    def test_encode_part(self):
        part = Part('Resistor', 'TestManufacturer', 'testPartNumber')
        series = Series('GR', 'Generic Resistor')
        part.add_series(series)
        reel = Reel(diameter=Dim(300, 'mm'), width=Dim(8, 'mm'))
        tape = Tape(tape_type='Paper', pin_1_quadrant='Q1', w=Dim(8,'mm'), e=None, f=None)
        packaging = TapeReelPackaging('R', 1000, reel, tape)
        order = OrderNumber('TestOrderNumber', packaging)
        order.production_status = 'Active'
        order.SKU = 'SKUTest'
        part.add_order_number(order)

        part_dict = part.to_dict()

        self.assertEqual(part_dict['partType'], 'Resistor')
        self.assertEqual(part_dict['manufacturer'], 'TestManufacturer')
        self.assertEqual(part_dict['partNumber'], 'testPartNumber')
        self.assertEqual(1, len(part_dict['series']))
        self.assertEqual('GR', part_dict['series'][0]['name'])
        self.assertEqual('Generic Resistor', part_dict['series'][0]['desc'])
        self.assertEqual('T', part_dict['series'][0]['generic'])

        self.assertEqual(part_dict['orderNumbers']['TestOrderNumber']['status'], 'Active')
        self.assertEqual(part_dict['orderNumbers']['TestOrderNumber']['SKU'], 'SKUTest')
        self.assertEqual(part_dict['orderNumbers']['TestOrderNumber']['type'], 'Tape/Reel')

        reel_dict = part_dict['orderNumbers']['TestOrderNumber']['packagingData']['reel']
        self.assertEqual('300mm', reel_dict['diameter'])
        self.assertEqual('8mm', reel_dict['width'])

        tape_dict = part_dict['orderNumbers']['TestOrderNumber']['packagingData']['tape']
        self.assertEqual('Paper', tape_dict['type'])
        self.assertEqual('Q1', tape_dict['pin_1_quadrant'])
        self.assertEqual('8mm', tape_dict['w'])

    def test_decode_part(self):
        part = Part('Resistor', 'TestManufacturer', 'testPartNumber')
        series = Series('GR', 'Generic Resistor')
        part.add_series(series)
        reel = Reel(diameter=Dim(300, 'mm'), width=Dim(8, 'mm'))
        tape = Tape(tape_type='Paper', pin_1_quadrant='Q1', w=Dim(8, 'mm'), e=None, f=None)
        packaging = TapeReelPackaging('R', 1000, reel, tape)
        order = OrderNumber('TestOrderNumber', packaging)
        order.production_status = 'Active'
        order.SKU = 'SKUTest'
        part.add_order_number(order)

        part_dict = part.to_dict()
        decoded_part = part_from_dict(part_dict)

        self.assertEqual(part.part_type, decoded_part.part_type)
        self.assertEqual(part.manufacturer, decoded_part.manufacturer)
        self.assertEqual(part.part_number, decoded_part.part_number)

    def test_order_number(self):
        order = OrderNumber('TestOrderNumber', None)
        order.production_status = 'Active'
        order.SKU = 'SKUTest'
        order_dict = order.to_dict()

        self.assertEqual(order_dict['status'], 'Active')
        self.assertEqual(order_dict['SKU'], 'SKUTest')
