
import unittest
import os
from AV.Reader.Reader import Reader


class ReaderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.reader = Reader(os.path.join(os.path.dirname(__file__), "..\\..\\..\\test_data\\Activiteitensheet 21.xlsx"))

    def test_get_sheet_list(self):
        sheets = self.reader.get_sheet_list()
        self.assertTrue('GBK' in sheets)
        self.assertTrue('Lid' in sheets)
        self.assertTrue('deb_specials' in sheets)
        self.assertTrue('AV Regels' in sheets)
        self.assertTrue('AV Regels compiled' in sheets)
        self.assertTrue('Voorbeeld' in sheets)
        self.assertTrue('Leeg' in sheets)
        self.assertTrue('CHECK' in sheets)



if __name__ == '__main__':
    unittest.main()
