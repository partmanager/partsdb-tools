from ..units.Value import Value as Dimension


class AxialTHTTape:
    #  |   |                         |   |
    #  |---|----------|||||----------|---|  --
    #  |   |                         |   |    S
    #  |---|----------|||||----------|---|  --
    #                   |
    #      | <---B1---> | <---B2---> |
    #      | <----------A----------> |
    #->| a |<-
    def __init__(self, tape_type, A:Dimension, a:Dimension, B1:Dimension, B2:Dimension, S: Dimension|None = None):
        self.tape_type = tape_type
        self.A = A
        self.a = a
        self.B1 = B1
        self.B2 = B2
        self.S = S

    def to_dict(self):
        result = {}
        if self.A:
            result['A'] = self.A.encode()
        if self.a:
            result['a'] = self.a.encode()
        if self.B1:
            result['B1'] = self.B1.encode()
        if self.B2:
            result['B2'] = self.B2.encode()
        if self.S:
            result['S'] = self.S.encode()
        return result