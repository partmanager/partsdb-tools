class Tape:
    def __init__(self, tape_type, pin_1_quadrant, w, e, f, so=None, d=None, t=None, p0=None, p1=None, p2=None, a0=None, b0=None, k=None):
        self.tape_type = tape_type
        self.pin_1_quadrant = pin_1_quadrant
        self.w = w
        self.e = e
        self.f = f
        self.so = so
        self.d = d
        self.t = t
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.a0 = a0
        self.b0 = b0
        self.k = k

    def to_dict(self):
        result = {}
        if self.pin_1_quadrant:
            result['pin_1_quadrant'] = self.pin_1_quadrant
        if self.w:
            result['w'] = self.w
        if self.e:
            result['e'] = self.e
        if self.f:
            result['f'] = self.f
        if self.so:
            result['so'] = self.so
        if self.d:
            result['d'] = self.d
        if self.t:
            result['t'] = self.t
        if self.p0:
            result['p0'] = self.p0
        if self.p1:
            result['p1'] = self.p1
        if self.p2:
            result['p2'] = self.p2
        if self.a0:
            result['a0'] = self.a0
        if self.b0:
            result['b0'] = self.b0
        if self.k:
            result['k'] = self.k
        return result


def tape_from_dict(tape_dict):
    tape = Tape(tape_dict['type'], pin_1_quadrant=None, w=None, e=None, f=None)
    if 'pin_1_quadrant' in tape_dict:
        tape.pin_1_quadrant = tape_dict['pin_1_quadrant']
    if 'w' in tape_dict:
        tape.w = tape_dict['w']
    if 'e' in tape_dict:
        tape.e = tape_dict['e']
    if 'f' in tape_dict:
        tape.f = tape_dict['f']
    if 'so' in tape_dict:
        tape.so= tape_dict['so']
    if 'd' in tape_dict:
        tape.d = tape_dict['d']
    if 't' in tape_dict:
        tape.t = tape_dict['t']
    if 'p0' in tape_dict:
        tape.p0 = tape_dict['p0']
    if 'p1' in tape_dict:
        tape.p1 = tape_dict['p1']
    if 'p2' in tape_dict:
        tape.p2 = tape_dict['p2']
    if 'a0' in tape_dict:
        tape.a0 = tape_dict['a0']
    if 'b0' in tape_dict:
        tape.b0 = tape_dict['b0']
    if 'k' in tape_dict:
        tape.k = tape_dict['k']
    return tape
