class Series:
    def __init__(self, name: str, description: str, manufacturer: str | None = None):
        self.name = name
        self.description = description
        self.manufacturer = manufacturer
        self.files = []

    def to_dict(self):
        result = {'name': self.name,
                  'desc': self.description}
        if self.manufacturer is None:
            result['generic'] = 'T'
        return result

def series_from_dict(series_dict, manufacturer):
    series = Series(series_dict['name'], series_dict['desc'])
    if 'generic' not in series_dict or series_dict['generic'] == 'F':
        series.manufacturer = manufacturer
    return series