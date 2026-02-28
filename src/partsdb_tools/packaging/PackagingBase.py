from decimal import Decimal


class PackagingBase:
    def __init__(self, code, qty: int | Decimal):
        self.code = code
        self.qty = qty

    def to_dict(self):
        raise NotImplementedError("Abstract method call, subclass shall implement to_dict method")

    def validate(self):
        raise NotImplementedError("Abstract method call, subclass shall implement validate method")
