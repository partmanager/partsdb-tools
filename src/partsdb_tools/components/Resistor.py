from .Part import Part


class Resistor(Part):
    def __init__(self, part_type, manufacturer, part_number):
        super().__init__(part_type, manufacturer, part_number)

    def validate(self):
        return super().validate()

    def validate_part_type(self):
        return self.part_type in ['Resistor', 'Resistor Thin Film', 'Resistor Thick Film', 'Resistor Metal Film',
                                  'Resistor Carbon Film']