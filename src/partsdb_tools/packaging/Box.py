from ..units.Value import Value as Dimension


class Box:
    def __init__(self, length: Dimension | None, width: Dimension | None, height: Dimension | None, weight=None):
        #      +-------+
        #     /       /| h
        #    /       / |
        #   +-------+  /
        #   |       | /  l
        #   |       |/
        #   +-------+
        #   <-- w -->
        self.length: Dimension | None = length
        self.width: Dimension | None = width
        self.height: Dimension | None = height
        self.weight = weight

    def to_dict(self):
        result = {
            'l': self.length.encode(),
            'w': self.width.encode(),
            'h': self.height.encode()
        }
        if self.weight:
            result['weight'] = self.weight
        return result

def box_from_dict(box_dict):
    box = Box(None, None, None)
    decoded = False
    if 'l' in box_dict:
        box.length = Dimension.decode(box_dict['l'])
        decoded = True
    if 'w' in box_dict:
        box.width = Dimension.decode(box_dict['w'])
        decoded = True
    if 'h' in box_dict:
        box.height = Dimension.decode(box_dict['h'])
        decoded = True
    if 'weight' in box_dict:
        box.weight = Dimension.decode(box_dict['weight'])
        decoded = True
    if decoded:
        return box
    return None