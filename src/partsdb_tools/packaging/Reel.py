from ..units.Value import Value as Dimension


class Reel:
    def __init__(self, diameter: Dimension, width: Dimension | None=None):
        self.diameter: Dimension = diameter
        self.width: Dimension = width

    def to_dict(self):
        result = {
            'diameter': self.diameter.encode()
        }
        if self.width:
            result['width'] = self.width.encode()
        return result


def reel_from_dict(reel_dict):
    if 'diameter' in reel_dict:
        reel = Reel(Dimension.decode(reel_dict['diameter']))
        if 'width' in reel_dict:
            reel.width = Dimension.decode(reel_dict['width'])
        return reel
    return None