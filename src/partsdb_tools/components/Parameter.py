class Parameter:
    def __init__(self, name, description, unit=None):
        self.name = name
        self.description = description
        self.unit = unit
        self.min = None
        self.typ = None
        self.max = None