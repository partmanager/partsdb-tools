import unittest
from src.partsdb_tools.packaging.from_dict import packaging_from_dict
from src.partsdb_tools.packaging.BoxPackaging import BoxPackaging
from src.partsdb_tools.packaging.BulkBoxPackaging import BulkBoxPackaging
from src.partsdb_tools.packaging.TapeBoxPackaging import TapeBoxPackaging
from src.partsdb_tools.packaging.TapeReelPackaging import TapeReelPackaging
from src.partsdb_tools.packaging.Box import Box
from src.partsdb_tools.packaging.Reel import Reel
from src.partsdb_tools.packaging.Tape import Tape


class Test(unittest.TestCase):
    def test_box_packaging(self):
        box = Box(length='10mm', width='5mm', height='2mm', weight=None)
        packaging = BoxPackaging('testCode', 3, box)
        packaging_dict = packaging.to_dict()

        self.assertEqual('Box', packaging_dict['type'])
        self.assertEqual('testCode', packaging_dict['code'])
        self.assertEqual(3, packaging_dict['qty'])
        self.assertEqual('10mm', packaging.box.length)
        self.assertEqual('5mm', packaging.box.width)
        self.assertEqual('2mm', packaging.box.height)

        packaging_decoded = packaging_from_dict(packaging_dict)
        self.assertIsInstance(packaging_decoded, BoxPackaging)
        self.assertEqual('Box', packaging_decoded.packaging_type)
        self.assertEqual('testCode', packaging_decoded.code)
        self.assertEqual(3, packaging_decoded.qty)

        self.assertIsInstance(packaging_decoded.box, Box)
        self.assertEqual('10mm', packaging_decoded.box.length)
        self.assertEqual('5mm', packaging_decoded.box.width)
        self.assertEqual('2mm', packaging_decoded.box.height)
        self.assertIsNone(packaging_decoded.box.weight)

    def test_bulk_box_packaging(self):
        box = Box(length='10mm', width='5mm', height='2mm', weight=None)
        packaging = BulkBoxPackaging('testCode', 3, box)
        packaging_dict = packaging.to_dict()

        self.assertEqual('Bulk/Box', packaging_dict['type'])
        self.assertEqual('testCode', packaging_dict['code'])
        self.assertEqual(3, packaging_dict['qty'])

        packaging_decoded = packaging_from_dict(packaging_dict)
        self.assertIsInstance(packaging_decoded, BulkBoxPackaging)
        self.assertEqual('Bulk/Box', packaging_decoded.packaging_type)
        self.assertEqual('testCode', packaging_decoded.code)
        self.assertEqual(3, packaging_decoded.qty)

        self.assertIsInstance(packaging_decoded.box, Box)
        self.assertEqual('10mm', packaging_decoded.box.length)
        self.assertEqual('5mm', packaging_decoded.box.width)
        self.assertEqual('2mm', packaging_decoded.box.height)
        self.assertIsNone(packaging_decoded.box.weight)

    def test_tape_box_packaging(self):
        packaging = TapeBoxPackaging('testCode', 3, None)
        packaging_dict = packaging.to_dict()

        self.assertEqual('Tape/Box', packaging_dict['type'])
        self.assertEqual('testCode', packaging_dict['code'])
        self.assertEqual(3, packaging_dict['qty'])

        packaging_decoded = packaging_from_dict(packaging_dict)
        self.assertIsInstance(packaging_decoded, TapeBoxPackaging)
        self.assertEqual('Tape/Box', packaging_decoded.packaging_type)
        self.assertEqual('testCode', packaging_decoded.code)
        self.assertEqual(3, packaging_decoded.qty)

    def test_tape_reel_packaging(self):
        reel = Reel(diameter='330mm', width='8mm')
        tape = Tape('Paper', 'Q1', w='8mm', e=None, f=None)
        packaging = TapeReelPackaging('testCode', 3, reel, tape)
        packaging_dict = packaging.to_dict()

        self.assertEqual('Tape/Reel', packaging_dict['type'])
        self.assertEqual('testCode', packaging_dict['code'])
        self.assertEqual(3, packaging_dict['qty'])
        self.assertEqual('330mm', packaging_dict['packagingData']['reel']['diameter'])
        self.assertEqual('8mm', packaging_dict['packagingData']['reel']['width'])
        self.assertEqual('Paper', packaging_dict['packagingData']['tape']['type'])
        self.assertEqual('Q1', packaging_dict['packagingData']['tape']['pin_1_quadrant'])
        self.assertEqual('8mm', packaging_dict['packagingData']['tape']['w'])

        packaging_decoded = packaging_from_dict(packaging_dict)
        self.assertIsInstance(packaging_decoded, TapeReelPackaging)
        self.assertEqual('Tape/Reel', packaging_decoded.packaging_type)
        self.assertEqual('testCode', packaging_decoded.code)
        self.assertEqual(3, packaging_decoded.qty)

        self.assertIsInstance(packaging_decoded.reel, Reel)
        self.assertEqual('330mm', packaging_decoded.reel.diameter)
        self.assertEqual('8mm', packaging_decoded.reel.width)

        self.assertIsInstance(packaging_decoded.tape, Tape)
        self.assertEqual('Paper', packaging_decoded.tape.tape_type)
        self.assertEqual('Q1', packaging_decoded.tape.pin_1_quadrant)
        self.assertEqual('8mm', packaging_decoded.tape.w)