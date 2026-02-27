from decimal import Decimal
from PackagingBase import PackagingBase
from .Reel import Reel
from .Tape import Tape


class TapeReelPackaging(PackagingBase):
    def __init__(self, code, qty: int | Decimal, reel: Reel | None, tape: Tape):
        super().__init__(code, qty)
        self.reel = reel
        self.tape = tape

    def to_dict(self):
        result = {
            'type': f"{self.tape.tape_type}/Reel",
            'code': self.code,
            'qty': self.qty
        }
        if self.reel and self.reel.to_dict():
            result['packagingData'] = {}
            result['packagingData']['reel'] = self.reel.to_dict()
        if self.tape.to_dict():
            if 'packagingData' not in result:
                result['packagingData'] = {}
            result['packagingData']['tape'] = self.tape.to_dict()
        return result
