from pathlib import Path
from ..detail.file_operations import calculate_md5


class Picture:
    def __init__(self, name: str, path: Path):
        self.name = name
        self.path = path
        self.md5 = None

    def calculate_md5(self):
        self.md5 = calculate_md5(self.path)