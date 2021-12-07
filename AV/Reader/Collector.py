from configparser import ConfigParser
import os.path as path
import openpyxl
import pandas as pd
from AV.Data.File import File

config = ConfigParser()
config.read(path.join(path.dirname(__file__), "../__conf__.ini"))


class Collector(object):

    def __init__(self, file: File):
        self.file = file
        self.config = file.config

    def load_data(self) -> pd.DataFrame:
        wb = openpyxl.load_workbook(self.file.path, read_only=True, data_only=True)
        ws: openpyxl.workbook.workbook.Worksheet = wb[self.file.active]
        df = pd.DataFrame(ws.values)[self.config.column_range]
        df.columns = df.iloc[int(self.config.header_index)-1]

        return df

    def collect_overzicht(self) -> pd.DataFrame:
        return self.load_data().loc[self.config.overzicht_range].dropna(how='all', thresh=4)

    def collect_afronding(self) -> pd.DataFrame:
        return self.load_data().loc[self.config.afronding_range].dropna(how='all')

    def collect_debiteuren(self) -> pd.DataFrame:
        return self.load_data().loc[self.config.debiteuren_start:].dropna(how='all')

    def collect_bp_range(self):
        return self.load_data().loc[self.config.bp_range]

    def collect_weekend_subsidie(self):
        return self.load_data().loc[[self.config.voorklim_index-1]]

