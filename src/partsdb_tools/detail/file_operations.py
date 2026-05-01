import json
from pathlib import Path


def load_json(file_path: Path):
    with open(file_path) as json_file:
        return json.load(json_file)
