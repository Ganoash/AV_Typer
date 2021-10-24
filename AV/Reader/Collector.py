from configparser import ConfigParser
import os.path as path
import openpyxl
import pandas as pd
from AV.ControllerData import ControllerData

config = ConfigParser()
config.read(path.join(path.dirname(__file__), "../__conf__.ini"))


class Collector(object):

    def __init__(self, data: ControllerData):
        self.data = data

    def load_data(self) -> pd.DataFrame:
        wb = openpyxl.load_workbook(self.data.file_path, read_only=True, data_only=True)
        ws: openpyxl.workbook.workbook.Worksheet = wb[self.data.sheet_name]
        df = pd.DataFrame(ws.values)[self.data.column_range]
        df.columns = df.iloc[int(self.data.header_index)-1]
        return df

    def collect_overzicht(self) -> pd.DataFrame:
        return self.load_data().loc[self.data.overzicht_range].dropna(how='all')

    def collect_afronding(self) -> pd.DataFrame:
        return self.load_data().loc[self.data.afronding_range].dropna(how='all')

    def collect_debiteuren(self) -> pd.DataFrame:
        return self.load_data().loc[self.data.debiteuren_start:].dropna(how='all')

