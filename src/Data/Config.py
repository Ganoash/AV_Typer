# standard library import
from os import path
from dataclasses import dataclass

# dependency imports
from configparser import ConfigParser

# package imports
from src.Data.SheetType import SheetType
from src.Utility import resource_path


@dataclass
class Config(object):
    """Dataclass representing a Config block

    This is a config object that will initialize itself based on it's SheetType, and subclass itself
    automatically where necessary. It reads data from __conf__.ini and represents it internally as an object.
    This object should be subclassed when a new type of config is desired. The bare minimum of config items that
    should be considered can be seen below.

    Attributes
    ----------
    type: SheetType
        the type of sheet
    filter: str
        a string representing the sheetnames that should be filtered in user selection
    column_range: list
        the relevant range of collumns that should be considered by the writer
    overzicht_range: list
        the "overzicht regels range" in the corresponding sheets
    afronding_range: list
        the "afronding regels range" in the corresponding sheets
    debiteuren_start: int
        the "debiteuren regel start index" in the corresponding sheets
    header_index: int
        the regel containing the headers

    Methods
    -------
    _initialize()
        Reads data from __conf.ini__ and populates class with it's data. Is called directly after initialization because
        of __post_init__
    reload_config()
        Calls _initialize again to reload data from config
    """

    type: SheetType = None
    filter: str = None
    column_range: list = None
    overzicht_range: list = None
    afronding_range: list = None
    debiteuren_start: int = None
    header_index: int = None

    def __new__(cls, type):
        """method for factory pattern-like subclassing

        automatically creates relevant subclass based on sheetType

        Parameters
        ----------
        type : SheetType
            Determines subclassing, properties, and property header read from __config__.ini

        """
        if type is SheetType.WEEKEND:
            return super(Config, WeekendConfig).__new__(WeekendConfig)
        if type is SheetType.BORREL or type is SheetType.ACTIVITEIT:
            return super(Config, BorrelConfig).__new__(BorrelConfig)
        return super(Config, cls).__new__(cls)

    def __post_init__(self):
        """method for initializing class data read from __config__.ini right after __init__"""
        self._initialize()

    def _initialize(self):
        """method for initializing class data read from __config__.ini right after __init__"""
        config = ConfigParser()
        config.read(resource_path("__conf__.ini"))
        self.config = config[str(self.type)]
        self.filter = self.config["filter"]
        self.column_range = list(
            range(
                int(self.config["column_range"].split(",")[0]) - 1,
                int(self.config["column_range"].split(",")[1]),
            )
        )
        self.overzicht_range = list(
            range(
                int(self.config["overzicht_range"].split(",")[0]) - 1,
                int(self.config["overzicht_range"].split(",")[1]),
            )
        )
        self.afronding_range = list(
            range(
                int(self.config["afronding_range"].split(",")[0]) - 1,
                int(self.config["afronding_range"].split(",")[1]),
            )
        )
        self.debiteuren_start = int(self.config["debiteuren_start"]) - 1
        self.header_index = int(self.config["header_index"])
        self.uitgaven_bank_boek_range = list(
            range(
                int(self.config["voorgeschoten_vanuit_bank_range"].split(",")[0]) - 1,
                int(self.config["voorgeschoten_vanuit_bank_range"].split(",")[1]),
            )
        )

    def reload_config(self):
        """reloads data from __config__.ini"""
        self._initialize()


class WeekendConfig(Config):
    """Datclass representing a weekend config block

    This is a config object representing the weekend block in __config__.ini. Adds functionality for voorklim_index

    Parameters
    ----------
    voorklim_index: int
        The row number in the weekendsheet containing data for voorklimsubsidie

    """

    voorklim_index: int = None

    def _initialize(self):
        super()._initialize()
        self.voorklim_index = int(self.config["voorklim_index"])


class BorrelConfig(Config):
    """Datclass representing a weekend config block

    This is a config object representing the borrel block in __config__.ini. Adds functionality for voorklim_index

    Parameters
    ----------
    bp_range: List
        The row numbers of the first and last row containing data for the bp credit for a borrel

    """

    bp_range: list = None

    def _initialize(self):
        super()._initialize()
        self.bp_range = list(
            range(
                int(self.config["bp_range"].split(",")[0]) - 1,
                int(self.config["bp_range"].split(",")[1]),
            )
        )
