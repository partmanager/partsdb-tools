from .PackageBase import PackageBase


class AxialResistorPackage(PackageBase):
    def __init__(self, name, length, diameter, lead_diameter, lead_length, lead_spacing):
        super().__init__("Axial Resistor", name)
        self.length = length
        self.diameter = diameter
        self.lead_diameter = lead_diameter
        self.lead_length = lead_length
        self.lead_spacing = lead_spacing

    def to_dict(self):
        result = {
            "type": self.package_type,
            "name": self.name,
            "dimensions": {
                "L": self.length,
                "D": self.diameter,
                "d": self.lead_diameter,
                "H": self.lead_length,
                "ls": self.lead_spacing
            }
        }
        return result