class OutputImageParameters:
    def __init__(self, width: int, height: int, border: int):
        assert width > 0 and height > 0
        assert border >= 0
        assert width - 2*border > 0
        assert height - 2*border > 0
        self.width = width
        self.height = height
        self.border = border
        self.ratio = width/height
        self.object_width = width - 2*border
        self.object_height = height - 2*border