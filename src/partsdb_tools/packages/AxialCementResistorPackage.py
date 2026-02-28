from .PackageBase import PackageBase


class AxialCementResistorPackage(PackageBase):
    def __init__(self, name, length, width, height, lead_diameter, lead_length, lead_spacing):
        super().__init__("Axial Cement Resistor", name)
        self.name = name
        self.length = length
        self.width = width
        self.height = height
        self.lead_diameter = lead_diameter
        self.lead_length = lead_length
        self.lead_spacing = lead_spacing

    def to_dict(self):
        result = {
            "type": self.package_type,
            "name": self.name,
            "dimensions": {
                "L": self.length,
                "W": self.width,
                "H": self.height,
                "d": self.lead_diameter,
                "ll": self.lead_length,
                "ls": self.lead_spacing
            }
        }
        return result