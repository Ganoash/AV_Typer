import tkinter
import openpyxl
from configparser import ConfigParser
from os import path
from enum import Enum, auto

class SheetType(Enum):
    ACTIVITEIT = auto()
    WEEKEND = auto()
    BORREL = auto()
    SIMPEL = auto()

    def __str__(self):
        if self is SheetType.ACTIVITEIT:
            return "activiteiten"
        elif self is SheetType.WEEKEND:
            return "weekend"
        elif self is SheetType.BORREL:
            return "borrel"
        elif self is SheetType.SIMPEL:
            return "simpel"


class ControllerData(object):

    def __init__(self):
        config = ConfigParser()
        config.read(path.join(path.dirname(__file__), "./__conf__.ini"))
        self.screen_types = ['select', 'type']
        self.current_screen = 'select'
        self.config = config
        self.sheet_types = list(str(st) for st in SheetType)
        self.file_path = ""

        self.sheet_type = SheetType.ACTIVITEIT
        self.sheet_name = ""

    @property
    def current_screen(self):
        return self._current_screen

    @current_screen.setter
    def current_screen(self, value):
        if value in self.screen_types:
            self._current_screen = value

    @property
    def sheet_type(self):
        return self._sheet_type

    @sheet_type.setter
    def sheet_type(self, sheet_type):
        if isinstance(sheet_type, str):
            for type in SheetType:
                if str(type) == sheet_type:
                    self._sheet_type = type
                    return
            raise ValueError('no config available for given sheet type')
        if isinstance(sheet_type, SheetType):
            self._sheet_type = sheet_type

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, value):
        if type(value) is tkinter.Entry:
            if self.validate_filename(value.get()):
                self._file_path = value.get()
        elif type(value) is str and value != "":
            if self.validate_filename(value):
                self._file_path = value
        else:
            self._file_path = ""

    @property
    def sheet_names(self):
        """
        Method for getting a list of sheets in
        the current workbook filters all workbooks that are in __conf__.ini
        :return: returns a list of sheets
        """
        if self.file_path == "":
            return []
        wb = openpyxl.load_workbook(self.file_path, read_only=True, data_only=True)
        sheets = wb.sheetnames
        wb.close()
        return list(filter(lambda sheet: sheet not in self.filter_sheets, sheets))



    @property
    def sheet_name(self):
        return self._sheet_name

    @sheet_name.setter
    def sheet_name(self, value):
        if value in self.sheet_names:
            self._sheet_name = value
        else:
            self._sheet_name = ""


    @property
    def sheet_set(self):
        return not len(self.sheet_names) == 0 and self.sheet_name in self.sheet_names

    @property
    def overzicht_range(self):
        if self.sheet_set:
            return list(range(int(self.config[str(self.sheet_type)]['overzicht_range'].split(',')[0]) - 1,
                              int(self.config[str(self.sheet_type)]['overzicht_range'].split(',')[1])))
        else:
            raise ValueError('Sheet is not set!')

    @property
    def column_range(self):
        if self.sheet_set:
            return list(range(int(self.config[str(self.sheet_type)]['column_range'].split(',')[0]),
                              int(self.config[str(self.sheet_type)]['column_range'].split(',')[1])))
        else:
            raise ValueError('Sheet is not set!')

    @property
    def afronding_range(self):
        if self.sheet_set:
            return list(range(int(self.config[str(self.sheet_type)]['afronding_range'].split(',')[0]) - 1,
                              int(self.config[str(self.sheet_type)]['afronding_range'].split(',')[1])))
        else:
            raise ValueError('Sheet is not set!')

    @property
    def debiteuren_start(self):
        if self.sheet_set:
            return int(self.config[str(self.sheet_type)]['debiteuren_start']) - 1
        else:
            raise ValueError('Sheet is not set!')

    @property
    def bp_range(self):
        if self.sheet_set and self.sheet_type is SheetType.BORREL:
            return list(range(int(self.config[str(self.sheet_type)]['bp_range'].split(',')[0]) - 1,
                              int(self.config[str(self.sheet_type)]['bp_range'].split(',')[1])))
    @property
    def weekend_subsidie_index(self):
        if self.sheet_set and self.sheet_type is SheetType.WEEKEND:
            return int(self.config[str(self.sheet_type)]['voorklim_index'])-1

    @property
    def header_index(self):
        if self.sheet_set:
            return self.config[str(self.sheet_type)]['header_index']
        else:
            raise ValueError('Sheet is not set!')

    @property
    def filter_sheets(self):
        if self.sheet_type is None:
            raise ValueError('No sheet_type is set!')
        return self.config[str(self.sheet_type)]['filter']

    def reload_config(self):
        config = ConfigParser()
        config.read(path.join(path.dirname(__file__), "../__conf__.ini"))
        self.config = config

    @staticmethod
    def validate_filename(file_name: str):
        if file_name is None:
            return False
        if not (file_name.endswith(".xlsx") or file_name.endswith(".xls")):
            return False
        try:
            data = open(file=file_name, mode='r')
            data.close()
            print(data)
            return True
        except FileNotFoundError:
            return False