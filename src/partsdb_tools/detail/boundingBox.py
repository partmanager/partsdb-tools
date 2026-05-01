
class BoundingBox:
    def __init__(self, xmin, xmax, ymin, ymax):
        assert xmin < xmax
        assert ymin < ymax
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.size_x = None
        self.size_y = None
        self.ratio = None
        self._update()

    def _update(self):
        self.size_x = self.xmax - self.xmin
        self.size_y = self.ymax - self.ymin
        self.ratio = self.size_x/self.size_y

    def center(self):
        return self.xmin + self.size_x / 2, self.ymin + self.size_y / 2

    def __str__(self):
        return f"Bounding box {self.xmin}-{self.xmax}-{self.ymin}-{self.ymax}"
