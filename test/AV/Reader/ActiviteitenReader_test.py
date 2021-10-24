import unittest
import os
import pandas as pd
from AV.Reader.Collector import Collector
from AV.Reader.Reader import Reader


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        test_data = os.path.join(os.path.dirname(__file__), "..\\..\\..\\test_data\\Activiteitensheet 21.xlsx")
        self.reader = Reader(test_data, 'activiteiten')
        self.collector = Collector(test_data, 'activiteiten')

    def test_get_sheet_list(self):
        sheets = self.reader.get_sheet_list()
        print(sheets)
        self.assertFalse('GBK' in sheets)
        self.assertFalse('Lid' in sheets)
        self.assertFalse('deb_specials' in sheets)
        self.assertFalse('AV Regels' in sheets)
        self.assertFalse('AV Regels compiled' in sheets)
        self.assertFalse('Voorbeeld' in sheets)
        self.assertFalse('Leeg' in sheets)
        self.assertFalse('CHECK' in sheets)

    def test_get_data(self):
        pd.set_option("display.max_rows", None, "display.max_columns", None)
        self.reader.set_sheet(self.reader.get_sheet_list()[0])
        print(self.reader.get_baten())



if __name__ == '__main__':
    unittest.main()
