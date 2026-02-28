class Reel:
    def __init__(self, diameter, width=None):
        self.diameter = diameter
        self.width = width

    def to_dict(self):
        result = {
            'diameter': self.diameter
        }
        if self.width:
            result['width'] = self.width
        return result


def reel_from_dict(reel_dict):
    if 'diameter' in reel_dict:
        reel = Reel(reel_dict['diameter'])
        if 'width' in reel_dict:
            reel.width = reel_dict['width']
        return reel
    return None