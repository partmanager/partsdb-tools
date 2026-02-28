from decimal import Decimal
from .PackagingBase import PackagingBase
from .Reel import Reel
from .Tape import Tape


class TapeReelPackaging(PackagingBase):
    def __init__(self, code, qty: int | Decimal, reel: Reel | None, tape: Tape):
        super().__init__('Tape/Reel', code, qty)
        self.reel = reel
        self.tape = tape

    def to_dict(self):
        result = super().to_dict()
        if self.reel and self.reel.to_dict():
            result['packagingData'] = {}
            result['packagingData']['reel'] = self.reel.to_dict()
        if self.tape and self.tape.to_dict():
            if 'packagingData' not in result:
                result['packagingData'] = {}
            result['packagingData']['tape'] = self.tape.to_dict()
        return result
