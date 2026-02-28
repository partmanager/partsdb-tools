from decimal import Decimal
from .PackagingBase import PackagingBase
from .Box import Box


class PaperTapeBoxPackaging(PackagingBase):
    def __init__(self, code, qty: int | Decimal, box: Box | None):
        super().__init__(code, qty)
        self.box = box
        self.tape = None

    def to_dict(self):
        result = {
            'type': "PaperTape/Box",
            'code': self.code,
            'qty': self.qty
        }
        if self.box and self.box.to_dict():
            result['packagingData'] = {}
            result['packagingData']['box'] = self.box.to_dict()
        if self.tape and self.tape.to_dict():
            if 'packagingData' not in result:
                result['packagingData'] = {}
            result['packagingData']['tape'] = self.tape.to_dict()
        return result
