from configparser import ConfigParser
from os import path

from AV.Data.SheetType import SheetType
from dataclasses import dataclass


@dataclass
class Config(object):
    type: SheetType = None
    filter: str = None
    column_range: list = None
    overzicht_range: list = None
    afronding_range: list = None
    debiteuren_start: int = None
    header_index: int = None

    def __new__(cls, type):
        if type is SheetType.BORREL:
            return super(Config, BorrelConfig).__new__(BorrelConfig)
        if type is SheetType.WEEKEND:
            return super(Config, WeekendConfig).__new__(WeekendConfig)
        return super(Config, cls).__new__(cls)

    def __post_init__(self):
        self._initialize()

    def _initialize(self):
        config = ConfigParser()
        config.read(path.join(path.dirname(__file__), "../__conf__.ini"))
        self.config = config[str(self.type)]
        self.filter = self.config['filter']
        self.column_range = list(range(int(self.config['column_range'].split(',')[0]) - 1,
                                          int(self.config['column_range'].split(',')[1])))
        self.overzicht_range = list(range(int(self.config['overzicht_range'].split(',')[0]) - 1,
                                          int(self.config['overzicht_range'].split(',')[1])))
        self.afronding_range = list(range(int(self.config['afronding_range'].split(',')[0]) - 1,
                                          int(self.config['afronding_range'].split(',')[1])))
        self.debiteuren_start = int(self.config['debiteuren_start']) - 1
        self.header_index = int(self.config['header_index'])

    def reload_config(self):
        self._initialize()


class WeekendConfig(Config):
    voorklim_index: int = None

    def _initialize(self):
        super()._initialize()
        self.voorklim_index = int(self.config['voorklim_index'])


class BorrelConfig(Config):
    bp_range: list = None

    def _initialize(self):
        super()._initialize()
        self.bp_range = list(range(int(self.config['bp_range'].split(',')[0]) - 1,
                                   int(self.config['bp_range'].split(',')[1])))
