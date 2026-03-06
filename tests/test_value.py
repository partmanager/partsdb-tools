import unittest
from src.partsdb_tools.units.Value import Value as Dim


class TestValue(unittest.TestCase):
    def test_encode_dimension(self):
        dim = Dim(123, 'mm')
        self.assertEqual('123mm', dim.encode())

        dim_tol = Dim(12, 'mm').tol(1,-1)
        self.assertEqual('12mm ±1', dim_tol.encode())

        dim_tol = Dim(12, 'mm').tol(1,-2)
        self.assertEqual('12mm -2/+1', dim_tol.encode())

        dim_tol = Dim(12, 'mm').tol(1, -0.5)
        self.assertEqual('12mm -0.5/+1', dim_tol.encode())

    def test_decode_dimension(self):
        dim_str = '123mm'
        dim = Dim.decode(dim_str)
        self.assertEqual(123, dim.value)
        self.assertEqual('mm', dim.unit)
        self.assertIsNone(dim.tolerance_neg)
        self.assertIsNone(dim.tolerance_pos)

        dim_str = '12mm ±1'
        dim = Dim.decode(dim_str)
        self.assertEqual(12, dim.value)
        self.assertEqual('mm', dim.unit)
        self.assertEqual(1, dim.tolerance_pos)
        self.assertEqual(1, dim.tolerance_neg)

        dim_str = '12mm -2/+1'
        dim = Dim.decode(dim_str)
        self.assertEqual(12, dim.value)
        self.assertEqual('mm', dim.unit)
        self.assertEqual(1, dim.tolerance_pos)
        self.assertEqual(-2, dim.tolerance_neg)

        dim_str = '12mm -0.5/+1'
        dim = Dim.decode(dim_str)
        self.assertEqual(12, dim.value)
        self.assertEqual('mm', dim.unit)
        self.assertEqual(1, dim.tolerance_pos)
        self.assertEqual(-0.5, dim.tolerance_neg)
