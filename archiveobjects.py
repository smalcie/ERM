from attributes import Attributes
from pathlib import Path
import datetime


class ArchiveData:
    # Container for storing archive object class objects
    _block_level = 1
    _block_level_indent = ' ' * _block_level * 2
    _class_name = 'Archive Data'
    _company_filter = '*'
    _folder_separator = '\\'
    _protection = 'OFF'

    def __init__(self, archive_object):
        if isinstance(archive_object, ArchiveObject):
            self.archive_objects = [archive_object]
        else:
            raise TypeError(f'{archive_object} is not an ArchiveObject type')

    def add_archive_object(self, archive_object):
        if isinstance(archive_object, ArchiveObject):
            getattr(self, archive_object).append(archive_object)
        else:
            raise TypeError(f'{archive_object} is not an ArchiveObject type')

    def copexify(self):
        copex = '::COPEX::\n'
        copex += f'{self._block_level_indent}Heading{self._block_level} "{self._class_name}"\n'
        copex += f'{self._block_level_indent}  CompanyFilter = {self._company_filter}\n'
        for archive_object in self.archive_objects:
            copex += archive_object.copexify()
        copex += '\n'
        copex += '::Goodbye::'
        return copex


class AOHeader:
    # todo put some documentation here
    _block_level = 3
    _parent_folders = {'petroleum reports': '/path/to/petroleum reports/',
                       'mineral drillhole samples': '/path/to/mineral drillhole samples/',
                       'petroleum drillhole samples': 'path/to/petroleum drillhole samples/',
                       }

    def __init__(self, ao_name, ao_type):
        self.ArchiveObjectName = ao_name
        self.Company = 'CROWN'
        self.ParentFolder = self.get_parent_folder(ao_type)
        self.Type = ao_type

    def __str__(self):
        return f'<{self.ArchiveObjectName}: {self.Type} {self.ParentFolder}>'

    def get_parent_folder(self, ao_type):
        return self._parent_folders[ao_type]

    def stringify(self, value):
        if ' ' in value:
            return f'"{str(value)}"'
        else:
            return str(value)

    def copexify(self):
        block_indent = ' '*self._block_level*2
        new_line = '\n'
        copex = f'{block_indent}Heading{self._block_level}: "Archive Object"{new_line}'
        for key, value in self.__dict__.items():
            copex += f'{block_indent}{block_indent[2:]}{key} = {self.stringify(value)}{new_line}'
        copex += new_line
        return copex

class Copex:
    _block_level = 0
    _indent = ' ' * _block_level * 2
    _type = ''
    _alt_operator = ''

    def copexify(self):
        copex = f'{self._indent}Heading{self._block_level}: {self.stringify(self._type)}\n'
        for key, value in self.__dict__.items():
            operator = '='
            if not key.startswith('_'):
                if key == self._alt_operator:
                    operator = ':='
                copex += f'{self._indent}  {key} {operator} {self.stringify(self.__getattribute__(key))}\n'
        return copex

    def stringify(self, value):
        # takes an object and
        if isinstance(value, int):
            return value
        elif isinstance(value, str) and ' ' not in value:
            return value
        elif isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, datetime.datetime):
            return datetime.datetime.strftime(value, '%d.%m.%Y')
        else:
            return value


class ArchiveObjectItem(Copex):
    # archive object component that stores file info
    _block_level = 3
    _indent = ' ' * _block_level * 2
    _type = 'Document Data'
    _alt_operator = 'ArchiveRef'
    _archive_paths = {'petroleum reports': '/data/archive/crown/Petroleum-Reports',
                      'mineral drillhole samples': '/data/archive/crown/Mineral-Drillhole-Samples',
                      'petroleum drillhole samples': '/data/archive/crown/Petroleum-Wellbore-Samples',
                        }

    def __init__(self, archive_object_type, archive_object_name, file_name, archive='NO', archive_am='online',
                 archive_type='disk', data_source='CROWN', storage_company='CROWN', storage_medium='file'):
        file = Path(self._archive_paths[archive_object_type]) / file_name
        self.ArchiveRef = file.__str__()
        self.Archive = archive
        self.ArchiveAm = archive_am
        self.ArchiveType = archive_type
        self.DataSource = data_source
        self.FileFmt = file.suffix[1:].upper()
        self.StorageCompany = storage_company
        self.StorageMedium = storage_medium
        self.Title = archive_object_name


class ArchiveObject:
    _block_level = 2

    def __init__(self, ao_name, ao_type, ao_file_name):
        self.ao_header = AOHeader(ao_name, ao_type)
        self.ao_item = ArchiveObjectItem(ao_name, ao_type, ao_file_name)

    def copexify(self):
        block_indent = ' '*self._block_level*2
        new_line = '\n'
        copex = f'{block_indent}Heading{self._block_level}: "Archive Data"{new_line}'
        for key, value in self.__dict__.items():
            copex += value.copexify()
        copex += new_line
        return copex





class LinkLicence(Copex):
    _block_level = 3
    _indent = ' ' * _block_level * 2
    _type = 'Link License'

    def __init__(self, licence):
        self.ID = licence


class LinkWell(Copex):
    _block_level = 3
    _indent = ' ' * _block_level * 2
    _type = 'Link Well'

    def __init__(self, well):
        self.PBWellID = well


def main():
    # ao = AOHeader('PR1234', 'petroleum reports')
    # print(ao)
    # print(ao.copexify())
    ao_item = ArchiveObjectItem('petroleum reports', 'PR1234', 'PR1234.pdf')
    print(ao_item.copexify())
    # archive_object = ArchiveObject('PR1234', 'petroleum reports', 'PR1234.pdf')
    # print(archive_object.copexify())
    # archive_data = ArchiveData(archive_object)
    # print(archive_data.copexify())
    link = LinkLicence(23456)
    print(link.copexify())
    link_well = LinkWell('NZ-WELL-1 ST1-ALL')
    print(link_well.copexify())


if __name__ == '__main__':
    main()