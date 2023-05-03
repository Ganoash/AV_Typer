# standard library imports
from typing import Tuple
import os.path as path

# dependency imports
import pandas as pd
from configparser import ConfigParser

# package imports
from src.Data.File import File
from src.Data.SheetType import SheetType
from src.Reader.Collector import Collector

config = ConfigParser()
config.read(path.join(path.dirname(__file__), "../__conf__.ini"))


class Reader(object):
    """Class for combining data to fit the needed output for Baten and Lasten

    The reader class combines various datablocks from the Collecter class to generate various baten and lasten
    regels needed for the input into AV. Subclassing is handled automatically using data from the file type
    This is the Reader class used to generate regels for Activiteitensheets

    Attributes
    ----------
    file
        File object the reader is reading
    collector
        collector object encapsulating the file

    Methods
    -------
    get_baten(self)
        Generates a pd.DataFrame containing the data for the baten rows
    get_lasten(self)
        Generates a pd.DataFrame containing the data for the lasten rows
    """

    def __new__(cls, file: File):
        if file.type is SheetType.BORREL:
            return super(Reader, BorrelReader).__new__(BorrelReader)
        if file.type is SheetType.WEEKEND:
            return super(Reader, WeekendReader).__new__(WeekendReader)
        if file.type is SheetType.SIMPEL:
            return super(Reader, SimpleReader).__new__(SimpleReader)
        else:
            return super(Reader, BorrelReader).__new__(BorrelReader)

    def __init__(self, file: File):
        self.file = file
        self.collector = Collector(file)

    def get_lasten(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Function for getting a dataframe with the compiled list of lasten regels
        :return: a dataframe containing all lastenregels from the compiled sheet
        :rtype: pd.DataFrame
        """
        if self.file.active is None:
            raise ValueError("Set an active sheet before getting the lasten!")

        # collect overzicht, filter alle niet lasten grootboeken, en format dataframe
        overzicht = self.collector.collect_overzicht()
        overzicht = (
            overzicht.loc[overzicht["GBK"].map(lambda c: str(c)[0] == "4")]
            .drop(["Credit", "Saldo"], axis=1)
            .rename({"Debit": "Bedrag"}, axis=1)
        )
        overzicht["GBK"] = overzicht["GBK"].astype(int)

        # collect debiteuren, filter diegene er uit die dingen hebben voorgeschoten format bedragen
        bijdragers = self.collector.collect_debiteuren()
        bijdragers: pd.DataFrame = bijdragers.loc[bijdragers["Credit"] != 0]
        bijdragers: pd.DataFrame = bijdragers.drop(["Debit", "Saldo"], axis=1).rename(
            {"Credit": "Bedrag"}, axis=1
        )
        bijdragers["Omschrijving"] = bijdragers["Omschrijving"].map(
            "Bijdrage {}".format
        )
        bijdragers["GBK"] = bijdragers["GBK"].astype(int)

        return overzicht, bijdragers

    def get_baten(self):
        """
        Function for getting a dataframe with the compiled list of baten regels
        :return: a dataframe containing all batenregels from the compiled sheet
        :rtype: pd.DataFrame
        """
        if self.file.active is None:
            raise ValueError("Set an active sheet before getting the baten!")

        # collect overzicht, filter alle niet baten grootboeken, en format dataframe
        overzicht = self.collector.collect_overzicht()
        print(overzicht)
        overzicht = (
            overzicht.loc[overzicht["GBK"].map(lambda c: str(c)[0] == "8")]
            .drop(["Credit", "Debit"], axis=1)
            .rename({"Saldo": "Bedrag"}, axis=1)
        )

        # collect winst door afronding en format dataframe
        winst_afronding = self.collector.collect_afronding()
        winst_afronding = winst_afronding.drop(["Credit", "Debit"], axis=1).rename(
            {"Saldo": "Bedrag"}, axis=1
        )

        # collect debiteuren en format bedragen
        debiteuren = self.collector.collect_debiteuren()
        debiteuren = debiteuren.drop(["Credit", "Saldo"], axis=1).rename(
            {"Debit": "Bedrag"}, axis=1
        )
        debiteuren["Omschrijving"] = debiteuren["Omschrijving"].map("Kosten {}".format)

        return pd.concat([overzicht, debiteuren, winst_afronding], axis=0)


class SimpleReader(Reader):
    """Class for combining data to fit the needed output for Baten and Lasten of simple workbooks

    The simple reader overwrites the interface of the reader to simply read the sheet as is and convert it
    to regels for AV

    Methods
    -------
    get_baten(self)
        Generates a pd.DataFrame containing the data in the sheet
    get_lasten(self)
        Generates a pd.DataFrame containing the data in the sheet
    """

    def get_lasten(self) -> pd.DataFrame:
        return self.get_baten()

    def get_baten(self):
        # collect debiteuren en format bedragen
        return self.collector.collect_debiteuren()


class BorrelReader(Reader):
    """Class for combining data to fit the needed output for Baten and Lasten of borrel workbooks

    Adds BP data to the lasten data of the Reader

    Methods
    -------
    get_lasten(self)
        Generates a pd.DataFrame containing the data in the sheet and data pertaining to BP contributions
    """

    def get_lasten(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        overzicht, bijdragers = super().get_lasten()
        bp_data: pd.DataFrame = self.collector.collect_bp_range()
        bp_line = (
            bp_data.drop(["Credit", "Debit"], axis=1)
            .rename({"Saldo": "Bedrag"}, axis=1)
            .iloc[[0]]
        )
        bp_line["Bedrag"] = bp_data["Saldo"].sum()
        bp_line.loc[:, "Omschrijving"] = "Credit BP " + self.file.active
        bp_line["GBK"] = bp_line["GBK"].astype(int)
        print(bp_line)
        print(bp_data)

        return overzicht, pd.concat([bp_line, bijdragers], axis=0)


class WeekendReader(Reader):
    """Class for combining data to fit the needed output for Baten and Lasten of weekend workbooks

    Adds voorklimsubsidie to the lasten data of the Reader

    Methods
    -------
    get_lasten(self)
        Generates a pd.DataFrame containing the data in the sheet and data pertaining to voorklim contributions
    """

    def get_lasten(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        overzicht, bijdragers = super().get_lasten()
        print(overzicht.columns)

        overzicht = overzicht[overzicht.Bedrag != 0]
        subsidie_data: pd.DataFrame = (
            self.collector.collect_weekend_subsidie()
            .drop(["Credit", "Saldo"], axis=1)
            .rename({"Debit": "Bedrag"}, axis=1)
        )
        subsidie_data["Omschrijving"] = "Voorklimsubsidie Yeti " + self.file.active
        print(subsidie_data)
        return pd.concat([overzicht, subsidie_data], axis=0), bijdragers
