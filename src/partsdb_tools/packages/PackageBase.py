class PackageBase:
    def __init__(self, package_type, name):
        self.package_type = package_type
        self.name = name

    def to_dict(self):
        raise NotImplementedError("Abstract method call, subclass shall implement to_dict method")

    def validate(self):
        raise NotImplementedError("Abstract method call, subclass shall implement validate method")