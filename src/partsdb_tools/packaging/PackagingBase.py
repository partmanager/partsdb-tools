from decimal import Decimal


class PackagingBase:
    def __init__(self, packaging_type, code, qty: int | Decimal):
        self.packaging_type = packaging_type
        self.code = code
        self.qty = qty

    def to_dict(self):
        result = {
            'type': self.packaging_type,
            'code': self.code,
            'qty': self.qty
        }
        return result

    def validate(self):
        raise NotImplementedError("Abstract method call, subclass shall implement validate method")
