from .PackageBase import PackageBase


class ChipResistorPackage(PackageBase):
    def __init__(self, name, length, width, height, t1, t2):
        super().__init__("Chip Resistor", name)
        self.length = length
        self.width = width
        self.height = height
        self.t1 = t1
        self.t2 = t2

    def to_dict(self):
        result = {
            "type": self.package_type,
            "name": self.name,
            "dimensions": {
                "l": self.length,
                "w": self.width,
                "h": self.height,
                "t1": self.t1,
                "t2": self.t2
            }
        }
        return result