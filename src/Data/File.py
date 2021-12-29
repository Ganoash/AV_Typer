# standard library imports
import tkinter
# dependency imports
import openpyxl
# package imports
from src.Data.Config import Config
from src.Data.SheetType import SheetType


class File(object):
    """File object representing an Excel sheet of some type

    This is a dataclass of the File of some workbook. It contains the path to the given workbook, the type of workbook
    it is, which sheet is currently active within the program, the config for the given type and the list of
    sheet_names the workbook contains

    Attributes
    ----------
    path: str
        The path to the workbook this object represents
    type: SheetType
        the type of workbook this object represents
    active: str
        which sheet is active within the workbook
    config: Config
        config for a workbook of this type
    active_set: bool
        returns true if and only if active is not an empty string
    """

    def __init__(self, path, type):
        self.path: str = path
        self.type: SheetType = type
        self.active: str = ""
        self.config: Config = Config(type)

        wb = openpyxl.load_workbook(self.path, read_only=True, data_only=True)
        self._sheet_names = list(filter(lambda sheet: sheet not in self.config.filter, wb.sheetnames))
        wb.close()

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = path

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type

    @property
    def sheet_names(self):
        return self._sheet_names

    def set_active(self, value):
        if value in self.sheet_names:
            self.active = value

    def active_set(self):
        return bool(self.active)


class FileBuilder:
    """Class for Building a File object step by step

    Provides type/format checking functionality for both parameters

    Attributes
    ----------
    path: str
        The path to the workbook the build file object represents
    type: SheetType
        the type of workbook the build file object represents

    Methods
    -------
    build()
        Builds a File object with the set path and type. Both should be set beforehand
    validate_path(file_name: str)
        Validates whether the given path is possible for a File object
    """

    def __init__(self):
        self.path = ""
        self.type = SheetType.ACTIVITEIT

    def set_path(self, path: str):
        if self.validate_path(path):
            self.path = path
            return True
        return False

    def set_type(self, t):
        print(t)
        print(type(t))
        if isinstance(t, SheetType):
            self.type = t
        elif isinstance(t, str):
            self.type = SheetType.from_string(t)
        elif isinstance(t, tkinter.Entry):
            self.type = SheetType.from_string(t.get())
            print(t)
            print(t.get())
        else:
            print("couldn't set type", t)
            return False
        return True

    def build(self):
        print(self.path, self.type)
        if self.path and self.type:
            return File(self.path, self.type)

    @staticmethod
    def validate_path(file_name: str):
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
