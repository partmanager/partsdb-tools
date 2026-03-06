from decimal import Decimal

class Value:
    def __init__(self, value, unit):
        self.value = value
        self.unit = unit
        self.tolerance_pos = None
        self.tolerance_neg = None

    def tol(self, pos, neg):
        self.tolerance_pos = pos
        self.tolerance_neg = neg
        return self

    def encode(self):
        result = f"{self.value}{self.unit}"
        if self.tolerance_neg and self.tolerance_pos:
            if abs(self.tolerance_pos) != abs(self.tolerance_neg):
                result += f" {self.tolerance_neg}/+{self.tolerance_pos}"
            else:
                result += f" ±{self.tolerance_pos}"
        return result

    @staticmethod
    def decode(value_str):
        tolerance_str = None
        unit = None
        if ' ' in value_str:
            value_str, tolerance_str = value_str.split(' ')
        for i, c in enumerate(value_str):
            if not c.isdigit():
                unit = value_str[i:]
                value_str = value_str[:i]
                break
        value = Value(Value.__value_from_str(value_str), unit)
        if tolerance_str:
            value._decode_tolerance(tolerance_str)

        return value

    @staticmethod
    def __value_from_str(value_str):
        if '.' in value_str:
            return Decimal(value_str)
        else:
            return int(value_str)

    def _decode_tolerance(self, tolerance_str):
        if '±' in tolerance_str:
            tol = self.__value_from_str(tolerance_str[1:])
            self.tolerance_pos = tol
            self.tolerance_neg = tol
        elif '/' in tolerance_str:
            tol_neg, tol_pos = tolerance_str.split('/')
            self.tolerance_neg = self.__value_from_str(tol_neg)
            self.tolerance_pos = self.__value_from_str(tol_pos)

