from .Part import Part
from .Parameter import Parameter


class Triac(Part):
    def __init__(self, part_type, manufacturer, part_number):
        super().__init__(part_type, manufacturer, part_number)
        self.parameters = {
            'V_gt': Parameter('V_gt', 'Gate threshold voltage'),
            'I_GT': Parameter('I_GT', 'Gate trigger current'),
            'V_DRM': Parameter('V_DRM', 'Repetitive peak off-state forward voltage'),
            'V_RRM': Parameter('V_RRM', 'Repetitive peak off-state reverse voltage'),
            'I_T': Parameter('I_T', 'RMS on-state current'),
            'I_TSM': Parameter('I_TSM', 'On-state current, non-repetitive peak'),
            'V_T': Parameter('V_T', 'On-state forward voltage'),
        }

    def validate(self):
        return super().validate()

    def validate_part_type(self):
        return self.part_type in ['Triac']