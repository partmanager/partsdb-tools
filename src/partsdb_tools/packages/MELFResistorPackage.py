from .PackageBase import PackageBase


class MELFResistorPackage(PackageBase):
    def __init__(self, name, length, diameter, electrode):
        super().__init__(package_type="MELF Resistor", name=name)
        self.length = length
        self.diameter = diameter
        self.electrode = electrode

    def to_dict(self):
        result = {
            "type": self.package_type,
            "name": self.name,
            "dimensions": {
                "L": self.length,
                "D": self.diameter,
                "k": self.electrode,
            }
        }
        return result