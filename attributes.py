import datetime
from archiveobjects import Copex


class Attributes(Copex):
    # Class variable that specifies fields
    _fields = {}
    _block_level = 3
    _indent = ' ' * _block_level * 2
    _type = ''

    def __init__(self, attributes_dict):
        # Set the arguments
        for key, value in attributes_dict.items():
            if key in self._fields.keys():
                setattr(self, key, value)

    # def serialise(self):
    #     print()
    #     for key, value in self._fields.items():
    #         if hasattr(self, key):
    #             print(f'{key} = {self.to_string(key)}')
    #     print()
    #
    # def to_string(self, name):
    #     # takes an object and
    #     if isinstance(getattr(self, name), int):
    #         return str(getattr(self, name))
    #     elif isinstance(getattr(self, name), str) and ' ' not in getattr(self, name):
    #         return getattr(self, name)
    #     elif isinstance(getattr(self, name), str):
    #         return f'"{getattr(self, name)}"'
    #     elif isinstance(getattr(self, name), datetime.date):
    #         return datetime.datetime.strftime(getattr(self, name), '%d.%m.%Y')
    #     else:
    #         return getattr(self, name)


class PetroleumWellboreSample(Attributes):
    # Class attributes for petroleum wellbore samples
    _type = 'petroleum wellbore samples'
    _fields = {'Box': 'str',
               'Boxes': 'str',
               'Date': 'datetime.datetime',
               'Depth_from': 'int',
               'Depth_to': 'int',
               'Interval': 'str',
               'Location': 'str',
               'Notes': 'str',
               'Operator': 'str',
               'Sample_ID': 'str',
               'Sample_Type': 'str',
               'Set': 'str',
               'Unit': 'str',
               'Well_Name': 'str'}


class PetroleumReport(Attributes):
    # Class attributes for petroleum reports archive object
    _type = 'petroleum reports'
    _fields = {'Report_Number': 'str',
               'Title': 'str',
               'Summary': 'str',
               'Licence': 'str',
               'End_Date': 'datetime.datetime',
               'Pages': 'str',
               'Location': 'str',
               'Notes': 'str',
               }


# class MSAtts(Attributes):
#     # Class attributes for mineral drillhole samples
#     pass


def main():
    params = {'Box': '1',
              'Boxes': '5',
              'Date': datetime.datetime(year=1990, month=2, day=5),
              'Depth_from': '230',
              'Depth_to': '240',
              'Interval': '10',
              'Location': 'over there'}
    print(params)
    att = PetroleumWellboreSample(params)
    print(att)
    att.copexify()
    # petroleum_report_attribute = {'Report_Number': '1234',
    #                               'Title': 'This is a report',
    #                               'Summary': 'Blah Blah Blah .......',
    #                               'Licence': '38254PEP',
    #                               'End_Date': datetime.datetime(year=1966, month=1, day=31),
    #                               'Pages': '25',
    #                               'Location': 'On the floor',
    #                               'Notes': 'This is a note about a report',
    #                               }
    # pratt = PRatts(petroleum_report_attribute)
    # # print(pratt)
    # pratt.serialise()


if __name__ == '__main__':
    main()
