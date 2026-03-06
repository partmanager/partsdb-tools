from ..units.Value import Value as Dimension


class Tape:
    def __init__(self, tape_type, pin_1_quadrant, w: Dimension, e: Dimension, f: Dimension, so=None, d=None, t=None, p0=None, p1=None, p2=None, a0=None, b0=None, k=None):
        self.tape_type = tape_type
        self.pin_1_quadrant = pin_1_quadrant
        self.w: Dimension = w
        self.e: Dimension = e
        self.f: Dimension = f
        self.so: Dimension | None = so
        self.d: Dimension | None = d
        self.t: Dimension | None = t
        self.p0: Dimension | None = p0
        self.p1: Dimension | None = p1
        self.p2: Dimension | None = p2
        self.a0: Dimension | None = a0
        self.b0: Dimension | None = b0
        self.k: Dimension | None = k

    def to_dict(self):
        result = {'type': self.tape_type}
        if self.pin_1_quadrant:
            result['pin_1_quadrant'] = self.pin_1_quadrant
        if self.w:
            result['w'] = self.w.encode()
        if self.e:
            result['e'] = self.e.encode()
        if self.f:
            result['f'] = self.f.encode()
        if self.so:
            result['so'] = self.so.encode()
        if self.d:
            result['d'] = self.d.encode()
        if self.t:
            result['t'] = self.t.encode()
        if self.p0:
            result['p0'] = self.p0.encode()
        if self.p1:
            result['p1'] = self.p1.encode()
        if self.p2:
            result['p2'] = self.p2.encode()
        if self.a0:
            result['a0'] = self.a0.encode()
        if self.b0:
            result['b0'] = self.b0.encode()
        if self.k:
            result['k'] = self.k.encode()
        return result


def tape_from_dict(tape_dict):
    tape = Tape(tape_dict['type'], pin_1_quadrant=None, w=None, e=None, f=None)
    if 'pin_1_quadrant' in tape_dict:
        tape.pin_1_quadrant = tape_dict['pin_1_quadrant']
    if 'w' in tape_dict:
        tape.w = Dimension.decode(tape_dict['w'])
    if 'e' in tape_dict:
        tape.e = Dimension.decode(tape_dict['e'])
    if 'f' in tape_dict:
        tape.f = Dimension.decode(tape_dict['f'])
    if 'so' in tape_dict:
        tape.so= Dimension.decode(tape_dict['so'])
    if 'd' in tape_dict:
        tape.d = Dimension.decode(tape_dict['d'])
    if 't' in tape_dict:
        tape.t = Dimension.decode(tape_dict['t'])
    if 'p0' in tape_dict:
        tape.p0 = Dimension.decode(tape_dict['p0'])
    if 'p1' in tape_dict:
        tape.p1 = Dimension.decode(tape_dict['p1'])
    if 'p2' in tape_dict:
        tape.p2 = Dimension.decode(tape_dict['p2'])
    if 'a0' in tape_dict:
        tape.a0 = Dimension.decode(tape_dict['a0'])
    if 'b0' in tape_dict:
        tape.b0 = Dimension.decode(tape_dict['b0'])
    if 'k' in tape_dict:
        tape.k = Dimension.decode(tape_dict['k'])
    return tape
