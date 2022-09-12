"""Constants for the library."""

from typing import Final

DEFAULT_TITLE: Final = "Notification"
DEFAULT_FONTSIZE: Final = "medium"
DEFAULT_POSITION: Final = "bottom-left"
DEFAULT_TRANSPARENCY: Final = "75%"
DEFAULT_COLOR: Final = "pink"
DEFAULT_INTERRUPT: Final = False
DEFAULT_ICON: Final = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGP6zwAAAgcBApo"
    "cMXEAAAAASUVORK5CYII="
)

BKG_COLORS: Final = {
    "grey": "#607d8b",
    "black": "#000000",
    "indigo": "#303F9F",
    "green": "#4CAF50",
    "red": "#F44336",
    "cyan": "#00BCD4",
    "teal": "#009688",
    "amber": "#FFC107",
    "pink": "#E91E63",
}
FONTSIZES: Final = {"small": 1, "medium": 0, "large": 2, "max": 3}
POSITIONS: Final = {
    "bottom-right": 0,
    "bottom-left": 1,
    "top-right": 2,
    "top-left": 3,
    "center": 4,
}

TRANSPARENCIES: Final = {
    "0%": 1,
    "25%": 2,
    "50%": 3,
    "75%": 4,
    "100%": 5,
}
