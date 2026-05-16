import argparse
from rich import print
from rich.console import Console
from rich.table import Table
from pathlib import Path
from .detail.file_operations import load_json
from .components.Part import Part, part_from_dict


def main():
    parser = argparse.ArgumentParser(description="Show part information. Part of part DB tools")
    parser.add_argument('-i', '--input', type=Path, help="Path to the input file (*.json)", required=True)
    args = parser.parse_args()

    part_json_data = load_json(args.input)
    part = part_from_dict(part_json_data, args.input)
    part.load_pictures()

    console = Console()

    console.print(part)
    console.print(create_pictures_table(part))
    console.print(create_attachment_table(part))


def create_pictures_table(part: Part):
    table = Table(title="Pictures")
    table.add_column('Name')
    table.add_column('md5')
    table.add_column('location')

    for picture in part.pictures:
        table.add_row(picture.name, picture.md5, str(picture.path))
    return table


def create_attachment_table(part: Part):
    table = Table(title="Attachments")
    table.add_column('Type')
    table.add_column('Name')
    table.add_column('Description')
    table.add_column('Version')
    table.add_column('Version date')
    table.add_column('md5')
    table.add_column('location')

    for attachment in part.files:
        table.add_row(attachment.type, attachment.filename, attachment.description)
        for key, version in attachment.versions.items():
            table.add_row(
                attachment.type,
                attachment.filename,
                attachment.description,
                version.revision,
                version.revision_date,
                version.md5sum,
                str(version.src_filepath)
            )
    return table