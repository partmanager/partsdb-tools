import json
import hashlib
from pathlib import Path


def load_json(file_path: Path):
    with open(file_path) as json_file:
        return json.load(json_file)

def find_file_by_md5sum(directory: Path, md5sum: str):
    results = []
    for file in Path(directory).rglob('*.*'):
        print(f"Checking: {file}, expected sum: {md5sum}")
        calculated = calculate_md5(file)
        print (calculated)
        if  calculated == md5sum:
            results.append(file)
    return results


def calculate_md5(filepath: Path):
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()
