import unittest
from src.partsdb_tools.components.Part import Part
from src.partsdb_tools.components.OrderNumber import OrderNumber


class Test(unittest.TestCase):
    def test(self):
        pass

    def test_encode_part(self):
        part = Part('Resistor', 'TestManufacturer', 'testPartNumber')
        part_dict = part.to_dict()

        self.assertEqual(part_dict['partType'], 'Resistor')
        self.assertEqual(part_dict['manufacturer'], 'TestManufacturer')
        self.assertEqual(part_dict['partNumber'], 'testPartNumber')

    def test_order_number(self):
        order = OrderNumber('TestOrderNumber', None)
        order.production_status = 'Active'
        order.SKU = 'SKUTest'
        order_dict = order.to_dict()

        self.assertEqual(order_dict['status'], 'Active')
        self.assertEqual(order_dict['SKU'], 'SKUTest')
