import datetime


class Copex:
    _block_level = 0
    _indent = ' ' * _block_level * 2
    _type = ''
    _alt_operator = ''

    def copexify(self):
        copex = f'{self._indent}Heading{self._block_level}: {self.stringify(self._type).title()}\n\n'
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
    _type = 'parameters petroleum wellbore samples'
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
    att = PetroleumWellboreSample(params)
    print(att.copexify())
    petroleum_report_attribute = {'Report_Number': '1234',
                                  'Title': 'This is a report',
                                  'Summary': 'Blah Blah Blah .......',
                                  'Licence': '38254PEP',
                                  'End_Date': datetime.datetime(year=1966, month=1, day=31),
                                  'Pages': '25',
                                  'Location': 'On the floor',
                                  'Notes': 'This is a note about a report',
                                  }
    pratt = PetroleumReport(petroleum_report_attribute)
    print(pratt.copexify())


if __name__ == '__main__':
    main()
