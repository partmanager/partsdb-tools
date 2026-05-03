import hashlib
import exiftool

from datetime import datetime, date
from pathlib import Path


class FileVersion:
    def __init__(self, url, filepath: Path, filename: str = None):
        self.filepath = filepath
        self.filename_org = filename if filename else None if self.filepath is None else self.filepath.name
        self.url = url
        self.latest: bool = False
        self.revision: str | None = None
        self.revision_date: date | None = None
        self.md5sum: str | None = None
        self._metadata: dict | None = None

    def validate(self):
        return self.md5sum == self._calculate_md5(self.filepath)

    def filename(self, manufacturer: str, part_number: str, extension: str):
        return f"{manufacturer.replace(' ', '_')}__{part_number}__{self.md5sum}.{extension}"

    def process_metadata(self):
        xmp = {}
        pdf = {}
        for k, v in self._metadata.items():
            print(f"{k} : {v}")
            if k.startswith('PDF:'):
                key = k[4:]
                pdf[key] = v
            if k.startswith("XMP:"):
                key = k[4:]
                xmp[key] = v
        dt = self._get_file_date(xmp, pdf)
        self.revision_date = dt.date()
        if self.revision is None:
            self.revision = self.revision_date.isoformat()

    def read_metadata(self):
        with exiftool.ExifToolHelper() as et:
            self._metadata = et.get_metadata(str(self.filepath))[0]

    def set_md5(self):
        self.md5sum = self._calculate_md5(self.filepath)
        return self.md5sum

    def to_dict(self):
        result = {
            'md5': self.md5sum,
        }
        if self.url:
            result['URL'] = self.url
        if self.revision_date:
            result['date'] = self.revision_date.isoformat()
        if self.filepath:
            result['filename'] = self.filename_org
        return result

    @staticmethod
    def _calculate_md5(filepath):
        with open(filepath, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    def _get_file_date(self, xmp, pdf) -> datetime:
        dates = []
        for field in ['ModifyDate', 'CreateDate', 'MetadataDate']:
            if field in xmp:
                dates.append(self._str_to_datetime(xmp[field]))

        for field in ['ModifyDate', 'CreateDate', 'MetadataDate']:
            if field in pdf:
                dates.append(self._str_to_datetime(pdf[field]))
        return max(dates)

    @staticmethod
    def _str_to_datetime(datetime_str: str):
        if ' ' in datetime_str:
            format_str = "%Y:%m:%d %H:%M:%S%z"
            dt = datetime.strptime(datetime_str, format_str)
        else:
            date_string = datetime_str.replace('Z', '+00:00')
            dt = datetime.fromisoformat(date_string)
        return dt


class PartFile:
    def __init__(self, file_type, filename: str, description: str, manufacturer: str):
        self.type = file_type
        self.filename: str = filename
        self.id: str | None = None
        self.description: str = description
        self.versions_supported = True
        self.versions: dict[str, FileVersion] = {}
        self.manufacturer = manufacturer

    def add_file_version(self, file_version):
        self.versions[file_version.revision] = file_version

    def to_dict(self):
        result = {"filename": self.filename}
        if self.description:
            result['desc'] = self.description
        if self.id:
            result['id'] = self.id
        if self.versions:
            result['versions'] = {}
            for key, version in self.versions.items():
                if version.latest:
                    result['url'] = version.url
                result['versions'][version.revision] = version.to_dict()
        return result

def attachment_file_from_dict(attachment_dict):
    attachment = PartFile(
        file_type=attachment_dict['type'],
        filename=attachment_dict['filename'],
        description=attachment_dict['desc'] if 'desc' in attachment_dict else None,
        manufacturer=None
    )

    if 'id' in attachment_dict:
        attachment.id = attachment_dict['id']

    if 'versions' in attachment_dict:
        for version_key in attachment_dict['versions']:
            version_dict = attachment_dict['versions'][version_key]
            url = None if 'URL' not in version_dict else version_dict['URL']
            version = FileVersion(url, None)
            version.revision = version_key
            version.md5sum = version_dict['md5']
            attachment.add_file_version(version)
    return attachment

