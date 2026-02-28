class AxialTHTTape:
    #  |   |                         |   |
    #  |---|----------|||||----------|---|  --
    #  |   |                         |   |    S
    #  |---|----------|||||----------|---|  --
    #                   |
    #      | <---B1---> | <---B2---> |
    #      | <----------A----------> |
    #->| a |<-
    def __init__(self, tape_type, A:float, a:float, B1:float, B2:float, S:float = None):
        self.tape_type = tape_type
        self.A = A
        self.a = a
        self.B1 = B1
        self.B2 = B2
        self.S = S

    def to_dict(self):
        result = {}
        if self.A:
            result['A'] = self.A
        if self.a:
            result['a'] = self.a
        if self.B1:
            result['B1'] = self.B1
        if self.B2:
            result['B2'] = self.B2
        if self.S:
            result['S'] = self.S
        return result