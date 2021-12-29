# standard library imports
from enum import Enum, auto

class SheetType(Enum):
    """Enumeration of the various types of sheets

    Currently supports for sheet types:
    Activiteiten sheets
    Weekend sheets
    Borrel sheets
    Simpel sheets (sheets with the headers at collumn A row 1, and all data below

    Methods
    -------
    __str__(self):
        function for SheetType to string conversion
    from_string(class, value):
        function for equivalent string to SheetType conversion
    """
    ACTIVITEIT = auto()
    WEEKEND = auto()
    BORREL = auto()
    SIMPEL = auto()

    def __str__(self):
        if self is SheetType.ACTIVITEIT:
            return "activiteiten"
        elif self is SheetType.WEEKEND:
            return "weekend"
        elif self is SheetType.BORREL:
            return "borrel"
        elif self is SheetType.SIMPEL:
            return "simpel"

    @classmethod
    def from_string(cls, value):
        for type in SheetType:
            if str(type) == value:
                return type