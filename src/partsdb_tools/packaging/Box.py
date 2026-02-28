class Box:
    def __init__(self, length, width, height, weight=None):
        #      +-------+
        #     /       /| h
        #    /       / |
        #   +-------+  /
        #   |       | /  l
        #   |       |/
        #   +-------+
        #   <-- w -->
        self.length = length
        self.width = width
        self.height = height
        self.weight = weight

    def to_dict(self):
        result = {
            'l': self.length,
            'w': self.width,
            'h': self.height
        }
        if self.weight:
            result['weight'] = self.weight
        return result

def box_from_dict(box_dict):
    box = Box(None, None, None)
    decoded = False
    if 'l' in box_dict:
        box.length = box_dict['l']
        decoded = True
    if 'w' in box_dict:
        box.width = box_dict['w']
        decoded = True
    if 'h' in box_dict:
        box.height = box_dict['h']
        decoded = True
    if 'weight' in box_dict:
        box.weight = box_dict['weight']
        decoded = True
    if decoded:
        return box
    return None