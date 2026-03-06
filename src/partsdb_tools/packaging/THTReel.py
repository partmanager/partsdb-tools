from ..units.Value import Value as Dimension


class THTReel:
    def __init__(self, diameter:Dimension, width:Dimension|None=None):
        self.diameter: Dimension = diameter
        self.width: Dimension = width

    def to_dict(self):
        result = {
            'diameter': self.diameter
        }
        if self.width:
            result['width'] = self.width
        return result