import unittest
from os import path
from src.Data.File import File
from src.Data.SheetType import SheetType
from src.Reader.Collector import Collector
import pandas as pd


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.weekend = File(
            path.join(
                path.dirname(__file__), "../../../test_data/Weekendsheet 21(1).xlsx"
            ),
            SheetType.WEEKEND,
        )
        self.activiteit = File(
            path.join(
                path.dirname(__file__), "../../../test_data/Activiteitensheet 21.xlsx"
            ),
            SheetType.ACTIVITEIT,
        )
        self.borrel = File(
            path.join(
                path.dirname(__file__), "../../../test_data/Borrelsheet 21(3).xlsx"
            ),
            SheetType.BORREL,
        )

        self.weekend.set_active(self.weekend.sheet_names[-1])
        self.activiteit.set_active(self.activiteit.sheet_names[-1])
        self.borrel.set_active(self.borrel.sheet_names[-1])

    def test_collect_overzicht(self):
        weekend = Collector(self.weekend)
        activiteit = Collector(self.activiteit)
        borrel = Collector(self.borrel)

        headers = [
            "Datum",
            "Deb_NR",
            "GBK",
            "Doc/fac",
            "Omschrijving",
            "Debit",
            "Credit",
            "Saldo",
        ]
        gbk_w = [8001, 5065, 4101, 4102, 4103, 4104, 4199]
        gbk_b = [4027, 8027]
        gbk_a = [4009, 8009]

        self.check(weekend.collect_overzicht(), headers, 7, gbk_w)
        self.check(borrel.collect_overzicht(), headers, 2, gbk_b)
        self.check(activiteit.collect_overzicht(), headers, 3, gbk_a)

    def test_collect_afronding(self):
        weekend = Collector(self.weekend)
        activiteit = Collector(self.activiteit)
        borrel = Collector(self.borrel)

        headers = [
            "Datum",
            "Deb_NR",
            "GBK",
            "Doc/fac",
            "Omschrijving",
            "Debit",
            "Credit",
            "Saldo",
        ]
        gbk_w = [5067]
        gbk_b = [5099]
        gbk_a = [5099]

        self.check(weekend.collect_afronding(), headers, 2, gbk_w)
        self.check(borrel.collect_afronding(), headers, 2, gbk_b)
        self.check(activiteit.collect_afronding(), headers, 2, gbk_a)

    def test_collect_debiteuren(self):
        weekend = Collector(self.weekend)
        activiteit = Collector(self.activiteit)
        borrel = Collector(self.borrel)

        headers = [
            "Datum",
            "Deb_NR",
            "GBK",
            "Doc/fac",
            "Omschrijving",
            "Debit",
            "Credit",
            "Saldo",
        ]
        gbk_w = [1300]
        gbk_b = [1300]
        gbk_a = [1300]

        debiteuren_w = [
            "9171087D",
            "9181131D",
            "9191150D",
            "915909D",
            "912627D",
            "911567D",
            "914793D",
            "9181144D",
        ]
        debiteuren_b = [
            "916998D",
            "9181128D",
            "9191211D",
            "9211283D",
            "9211259D",
            "913672D",
            "914775D",
            "9191211D",
            "913674D",
            "915893D",
            "9191188D",
            "9211252D",
            "9211275D",
            "9161005D",
            "9201228D",
        ]
        debiteuren_a = [
            "9181113D",
            "9211276D",
            "9191188D",
            "9201228D",
            "9181144D",
            "9211275D",
            "9171037D",
            "9181128D",
            "9191211D",
            "915901D",
            "916997D",
            "9181131D",
            "9181132D",
        ]
        self.check(weekend.collect_debiteuren(), headers, 8, gbk_w, debiteuren_w)
        self.check(borrel.collect_debiteuren(), headers, 15, gbk_b, debiteuren_b)
        self.check(activiteit.collect_debiteuren(), headers, 13, gbk_a, debiteuren_a)

    def test_collect_bp(self):
        borrel = Collector(self.borrel)
        weekend = Collector(self.weekend)

        headers = [
            "Datum",
            "Deb_NR",
            "GBK",
            "Doc/fac",
            "Omschrijving",
            "Debit",
            "Credit",
            "Saldo",
        ]
        gbk = [1300]
        deb = ["904097D"]

        self.check(borrel.collect_bp_range(), headers, 3, gbk, deb)
        self.failUnlessRaises(AttributeError, weekend.collect_bp_range)

    def test_collect_voorklim_subsidie(self):
        borrel = Collector(self.borrel)
        weekend = Collector(self.weekend)

        headers = [
            "Datum",
            "Deb_NR",
            "GBK",
            "Doc/fac",
            "Omschrijving",
            "Debit",
            "Credit",
            "Saldo",
        ]
        gbk = [5065]

        self.check(weekend.collect_weekend_subsidie(), headers, 1, gbk)
        self.failUnlessRaises(AttributeError, borrel.collect_weekend_subsidie)

    def check(
        self,
        frame: pd.DataFrame,
        headers: list,
        length: int,
        GBK: list,
        debiteuren: list = None,
    ):
        print(frame)
        for header in headers:
            self.assertIn(header, frame.columns)

        for gbk in GBK:
            self.assertIn(gbk, frame["GBK"].to_list())

        self.assertEqual(len(frame.index), length)

        if debiteuren:
            for deb in debiteuren:
                self.assertIn(deb, frame["Deb_NR"].to_list())
        else:
            for deb in frame["Deb_NR"].to_list():
                self.assertIsNone(deb)


if __name__ == "__main__":
    unittest.main()
