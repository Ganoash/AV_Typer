# standard library imports
import os.path as path

# dependency imports
import openpyxl
import pandas as pd
from configparser import ConfigParser

# package imports
from src.Data.File import File
from src.Utility import resource_path

# read config
config = ConfigParser()
config.read(resource_path("__conf__.ini"))


class Collector(object):
    """Class for collecting data from a given File object

    provides an interface to get discrete datablocks from various types of sheets.

    Attributes
    ----------
    file: File
        The file data should be collected from
    config: Config
        config for the given FileType

    Methods
    -------
    load_data(self)
        loads data from the workbook the file is referencing, returns a dataframe containing it
    collect_overzicht(self)
        returns the data containing pertaining overzicht
    collect_afronding(self)
        returns the data pertaining afronding
    collect_debiteuren(self)
        returns the data pertaining to debiteuren
    collect_bp_range(self)
        returns the data pertaining to BP stand for borrels. Only defined for files of type BORREL
    collect_weekend_subsidie(self)
        returns the data pertaining to voorklimsubsidie. only defined for files of type WEEKEND
    """

    def __init__(self, file: File):
        self.file = file
        self.config = file.config

    def load_data(self) -> pd.DataFrame:
        wb = openpyxl.load_workbook(self.file.path, read_only=True, data_only=True)
        ws: openpyxl.workbook.workbook.Worksheet = wb[self.file.active]
        df = pd.DataFrame(ws.values)[self.config.column_range]
        df.columns = df.iloc[int(self.config.header_index) - 1]

        return df

    def collect_overzicht(self) -> pd.DataFrame:
        return self.load_data().loc[self.config.overzicht_range].dropna(how="all")

    def collect_afronding(self) -> pd.DataFrame:
        return self.load_data().loc[self.config.afronding_range].dropna(how="all")

    def collect_debiteuren(self) -> pd.DataFrame:
        return self.load_data().loc[self.config.debiteuren_start :].dropna(how="all")

    def collect_bp_range(self):
        return self.load_data().loc[self.config.bp_range]

    def collect_uitgaven_bankboek(self):
        return self.load_data().loc[self.config.uitgaven_bank_boek_range]

    def collect_weekend_subsidie(self):
        return self.load_data().loc[[self.config.voorklim_index - 1]]
