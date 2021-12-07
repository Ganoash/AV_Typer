from enum import Enum, auto

class SheetType(Enum):
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