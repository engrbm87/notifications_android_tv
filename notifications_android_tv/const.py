"""Constants for the library."""

from enum import Enum, IntEnum
from typing import Final

DEFAULT_TITLE: Final = "Notification"
DEFAULT_ICON: Final = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGP6zwAAAgcBApo"
    "cMXEAAAAASUVORK5CYII="
)


class BkgColors(Enum):
    """Background color options."""

    GREY = "#607d8b"
    BLACK = "#000000"
    INDIGO = "#303F9F"
    GREEN = "#4CAF50"
    RED = "#F44336"
    CYAN = "#00BCD4"
    TEAL = "#009688"
    AMBER = "#FFC107"
    PINK = "#E91E63"


class FontSizes(IntEnum):
    """Supported font sizes for notification text."""

    SMALL = 1
    MEDIUM = 0
    LARGE = 2
    MAX = 3


class Positions(IntEnum):
    """Supported positions for the notification overlay."""

    BOTTOM_RIGHT = 0
    BOTTOM_LEFT = 1
    TOP_RIGHT = 2
    TOP_LEFT = 3
    CENTER = 4


class Transparencies:
    """Supported transparencies for the notification overlay.

    Supported values:
      - 0%
      - 25%
      - 50%
      - 75%
      - 100%
    """

    @classmethod
    def from_percentage(cls, percentage: str) -> int:
        """Convert percentage to int."""
        _mapping = {"0%": 1, "25%": 2, "50%": 3, "75%": 4, "100%": 5}
        return _mapping.get(percentage, 1)
