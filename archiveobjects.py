from attributes import Copex, PetroleumWellboreSample
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
        copex = '::COPEX::\n\n'
        copex += f'{self._block_level_indent}Heading{self._block_level} "{self._class_name}"\n\n'
        copex += f'{self._block_level_indent}  CompanyFilter = {self._company_filter}\n'
        copex += f'{self._block_level_indent}  FolderSeparator = {self._folder_separator}\n'
        copex += f'{self._block_level_indent}  Protection = {self._protection}\n\n'
        for archive_object in self.archive_objects:
            copex += archive_object.copexify()
        copex += '::Goodbye::'
        return copex


class ArchiveObjectHeader(Copex):
    # todo put some documentation here
    _block_level = 2
    _indent = ' ' * _block_level * 2
    _type = 'archive object'
    _alt_operator = 'ArchiveObjectName'
    _parent_folders = {'petroleum reports': '/path/to/petroleum reports/',
                       'mineral drillhole samples': '/path/to/mineral drillhole samples/',
                       'petroleum wellbore samples': 'PETROLEUM\PETROLEUM-WELLBORE-SAMPLES',
                       }

    def __init__(self, archive_object_type, archive_object_name,  company='CROWN'):
        self.ArchiveObjectName = archive_object_name
        self.Company = company
        self.ParentFolder = self.get_parent_folder(archive_object_type)
        self.Type = archive_object_type

    def __str__(self):
        return f'<{self.ArchiveObjectName}: {self.Type} {self.ParentFolder}>'

    def get_parent_folder(self, archive_object_type):
        return self._parent_folders[archive_object_type]



class ArchiveObjectItem(Copex):
    # archive object component that stores file info
    _block_level = 3
    _indent = ' ' * _block_level * 2
    _type = 'Document Data'
    _alt_operator = 'ArchiveRef'
    _archive_paths = {'petroleum reports': '/data/archive/crown/Petroleum-Reports',
                      'mineral drillhole samples': '/data/archive/crown/Mineral-Drillhole-Samples',
                      'petroleum wellbore samples': '/data/archive/crown/Petroleum-Sample-Images',
                        }

    def __init__(self, archive_object_type, archive_object_name,
                 archive_object_file_name, archive='NO', archive_am='online',
                 archive_type='disk', data_source='CROWN', storage_company='CROWN',
                 storage_medium='file'):
        full_file_path = Path(self._archive_paths[archive_object_type]) / archive_object_file_name
        self.ArchiveRef = full_file_path.__str__()
        self.Archive = archive
        self.ArchiveAm = archive_am
        self.ArchiveType = archive_type
        self.DataSource = data_source
        self.FileFmt = full_file_path.suffix[1:].upper()
        self.StorageCompany = storage_company
        self.StorageMedium = storage_medium
        self.Title = archive_object_name


class ArchiveObject(Copex):
    _block_level = 2
    _indent = ' ' * _block_level * 2
    _type = 'archive object'
    _alt_operator = 'ArchiveObjectName'
    _parent_folders = {'petroleum reports': '/path/to/petroleum reports/',
                       'mineral drillhole samples': '/path/to/mineral drillhole samples/',
                       'petroleum wellbore samples': 'PETROLEUM\PETROLEUM-WELLBORE-SAMPLES',
                       }

    def __init__(self, type, name, file, attributes, licence, well):
        self.header = ArchiveObjectHeader(type, name)
        self.item = ArchiveObjectItem(type, name, file)
        self.attributes = PetroleumWellboreSample(attributes)
        self.linkcountry = LinkCountry('NEW ZEALAND')
        self.linklicence = LinkLicence(licence)
        self.linkwell = LinkWell(well)

    def copexify(self):
        copex = ''
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                copex += value.copexify()
            copex += '\n'
        return copex


class LinkCountry(Copex):
    _block_level = 3
    _indent = ' ' * _block_level * 2
    _type = 'Link Country'

    def __init__(self, licence):
        self.ID = licence

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
    well = 'NZ-WELL-1 ST1-ALL'
    attributes = {'Box': '1',
                  'Boxes': '5',
                  'Date': datetime.datetime(year=1990, month=2, day=5),
                  'Depth_from': '230',
                  'Depth_to': '240',
                  'Interval': '10',
                  'Location': 'over there'}
    archive_object = ArchiveObject('petroleum wellbore samples', 'Petroleum Sample 52107', '52107.JPG', attributes, 381258, well)
    data = ArchiveData(archive_object)
    print(data.copexify())


if __name__ == '__main__':
    main()