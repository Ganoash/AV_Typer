import datetime

import openpyxl
import pandas
import pandas as pd
from typing import Tuple
from configparser import ConfigParser
import os.path as path

from AV.Reader.Collector import Collector
from AV.ControllerData import ControllerData

config = ConfigParser()
config.read(path.join(path.dirname(__file__), "../__conf__.ini"))


class Reader(object):
    def __init__(self, data: ControllerData):
        self.data = data
        self.collector = Collector(data)

    def get_lasten(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Function for getting a dataframe with the compiled list of lasten regels
        :return: a dataframe containing all lastenregels from the compiled sheet
        :rtype: pd.DataFrame
        """
        if self.data.sheet_name is None:
            raise ValueError('Set an active sheet before getting the lasten!')

        # collect overzicht, filter alle niet lasten grootboeken, en format dataframe
        overzicht = self.collector.collect_overzicht()
        overzicht = overzicht.loc[overzicht["GBK"].map(lambda c: str(c)[0] == '4')] \
            .drop(['Credit', 'Saldo'], axis=1) \
            .rename({'Debit': 'Bedrag'}, axis=1)

        # collect debiteuren, filter diegene er uit die dingen hebben voorgeschoten format bedragen
        bijdragers = self.collector.collect_debiteuren()
        bijdragers: pd.DataFrame = bijdragers.loc[bijdragers['Credit'] != 0]
        bijdragers: pd.DataFrame = bijdragers.drop(['Debit', 'Saldo'], axis=1).rename({'Credit': 'Bedrag'}, axis=1)
        bijdragers["Omschrijving"] = bijdragers["Omschrijving"].map("Bijdrage {}".format)

        return overzicht, bijdragers

    def get_baten(self):
        """
        Function for getting a dataframe with the compiled list of baten regels
        :return: a dataframe containing all batenregels from the compiled sheet
        :rtype: pd.DataFrame
        """
        if self.data.sheet_name is None:
            raise ValueError('Set an active sheet before getting the baten!')

        # collect overzicht, filter alle niet baten grootboeken, en format dataframe
        overzicht = self.collector.collect_overzicht()
        print(overzicht)
        overzicht = overzicht.loc[overzicht["GBK"].map(lambda c: str(c)[0] == '8')] \
            .drop(['Credit', 'Debit'], axis=1) \
            .rename({'Saldo': 'Bedrag'}, axis=1)

        # collect winst door afronding en format dataframe
        winst_afronding = self.collector.collect_afronding()
        winst_afronding = winst_afronding.drop(['Credit', 'Debit'], axis=1).rename({'Saldo': 'Bedrag'}, axis=1)

        # collect debiteuren en format bedragen
        debiteuren = self.collector.collect_debiteuren()
        debiteuren = debiteuren.drop(['Credit', 'Saldo'], axis=1).rename({'Debit': 'Bedrag'}, axis=1)
        debiteuren["Omschrijving"] = debiteuren["Omschrijving"].map("Kosten {}".format)

        return pd.concat([overzicht, debiteuren, winst_afronding], axis=0)


class Simple_Reader(Reader):
    'Reader voor het uitlezen van simpele regel bestanden'

    def __init__(self, data: ControllerData):
        super().__init__(data)

    def get_lasten(self) -> pd.DataFrame:
        return self.get_baten()

    def get_baten(self):
        # collect debiteuren en format bedragen
        return self.collector.collect_debiteuren()


class Borrel_Reader(Reader):

    def __init__(self, data: ControllerData):
        super().__init__(data)

    def get_lasten(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        overzicht, bijdragers = super().get_lasten()
        bp_data: pd.DataFrame = self.collector.collect_bp_range()
        bp_line = bp_data.drop(['Credit', 'Debit'], axis=1)\
            .rename({'Saldo': 'Bedrag'}, axis=1).iloc[[0]]
        bp_line['Bedrag'] = bp_data['Saldo'].sum()
        bp_line.loc[:, "Omschrijving"] = "Credit BP " + self.data.sheet_name
        print(bp_line)
        print(bp_data)


        return overzicht, pd.concat([bp_line, bijdragers], axis=0)


class Weekend_Reader(Reader):
    def __init__(self, data: ControllerData):
        super().__init__(data)

    def get_lasten(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        overzicht, bijdragers = super().get_lasten()
        print(overzicht.columns)

        overzicht = overzicht[overzicht.Bedrag != 0]
        subsidie_data: pd.DataFrame = self.collector.collect_weekend_subsidie()\
            .drop(['Credit', 'Saldo'], axis=1)\
            .rename({'Debit': 'Bedrag'}, axis=1)
        subsidie_data["Omschrijving"] = "Voorklimsubsidie Yeti " + self.data.sheet_name
        print(subsidie_data)
        return pd.concat([overzicht, subsidie_data], axis=0), bijdragers
