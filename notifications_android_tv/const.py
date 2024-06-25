"""Constants for the library."""

from enum import Enum, IntEnum
from typing import Final


class BkgColor(Enum):
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


class FontSize(IntEnum):
    """Supported font sizes for notification text."""

    SMALL = 1
    MEDIUM = 0
    LARGE = 2
    MAX = 3


class Position:
    """Position of the notification.

    Supported values:
      - 0: Bottom right
      - 1: Bottom left
      - 2: Top right
      - 3: Top left
      - 4: Center
    """

    @classmethod
    def from_string(cls, position: str) -> int:
        """Convert position to int."""
        _mapping = {
            "bottom-right": 0,
            "bottom-left": 1,
            "top-right": 2,
            "top-left": 3,
            "center": 4,
        }
        return _mapping.get(position, 0)


class Transparency:
    """Transparency for the notification overlay.

    Supported values:
      - 1: 0%
      - 2; 25%
      - 3: 50%
      - 4: 75%
      - 5: 100%
    """

    @classmethod
    def from_percentage(cls, percentage: str) -> int:
        """Convert percentage to int."""
        _mapping = {
            "0%": 1,
            "25%": 2,
            "50%": 3,
            "75%": 4,
            "100%": 5,
        }
        return _mapping.get(percentage, 1)


DEFAULT_TITLE: Final = "Notification"
DEFAULT_DURATION: Final = 5
DEFAULT_POSITION: Final = 0
DEFAULT_BKGCOLOR: Final = BkgColor.GREY
DEFAULT_FONTSIZE: Final = FontSize.MEDIUM
DEFAULT_TRANSPARENCY: Final = 1
DEFAULT_ICON: Final = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGP6zwAAAgcBApo"
    "cMXEAAAAASUVORK5CYII="
)
