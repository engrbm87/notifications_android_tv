import base64
import io
import logging
from typing import Final

import requests
from requests.exceptions import ConnectionError, ConnectTimeout

_LOGGER = logging.getLogger(__name__)


class Notifications:

    PORT: Final = 7676

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
    DEFAULT_TITLE: Final = "Notification"
    DEFAULT_DURATION: Final = 5
    DEFAULT_FONTSIZE: Final = "medium"
    DEFAULT_POSITION: Final = "bottom-left"
    DEFAULT_TRANSPARENCY: Final = "75%"
    DEFAULT_COLOR: Final = "pink"
    DEFAULT_INTERRUPT: Final = False
    DEFAULT_TIMEOUT: Final = 5
    DEFAULT_ICON: Final = (
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGP6zwAAAgcBApo"
        "cMXEAAAAASUVORK5CYII="
    )
    def __init__(self, host: str) -> None:
        """Initialize notifier."""
        self.url = f"http://{host}:7676"
        try:
            requests.get(self.url, timeout=self.DEFAULT_TIMEOUT)
        except (ConnectionError, ConnectTimeout) as err:
            _LOGGER.error("Error communicating with %s: %s", self.url, str(err))
            raise ConnectError from err

    def send(
        self,
        message,
        title: str = None,
        duration: int = None,
        fontsize: str = None,
        position: str = None,
        bkgcolor: str = None,
        transparency: str = None,
        interrupt: bool = False,
        icon: bytes = None,
        image_file: bytes = None,
    ) -> bool:
        """Send message with parameters.
        :param message: The notification message.
        :param title: (Optional) The notification title.
        :param duration: (Optional) Display the notification for the specified period.
            Default duration is 5 seconds.
        :param fontsize: (Optional) Specify text font size (`small`, `medium`, `large`, `max`).
        :param position: (Optional) Specify notification position (`bottom-right`, `bottom-left`,
            `top-right`, `top-left`, `center`). Default is `bottom-right`.
        :param bkgcolor: (Optional) Specify background color. Can be one of (`grey`, `black`, `indigo`,
            `green`, `red`, `cyan`, `teal`, `amber`, `pink`). Default is `grey`.
        :param transparency: (Optional) Specify the background transparency of the notification.
            Can be one of (`0%`, `25%`, `50%`, `75%`, `100%`). Default is `0%`.
        :param interrupt: (Optional) Setting it to true makes the notification interactive 
            and can be dismissed or selected to display more details. Default is False
        :param icon: (Optional) Attach icon to notification. Type must be `bytes`.
        :param image_file: (Optional) Attach image to notification. Type must be `bytes`.
        Usage::

        >>> from notifications_android_tv import Notifications  
        >>> notifier = Notifications("192.168.3.88")
        >>> notifier.send(
                "message to be sent", 
                title="Notification title",
                duration="20", 
                transparency="100%"
            )
        <Response True>
        """
        payload = {
            "filename": (
                "icon.png",
                io.BytesIO(base64.b64decode(self.DEFAULT_ICON)),
                "application/octet-stream",
                {"Expires": "0"},
            ),
            "msg": message,
        }
        if title:
            payload["title"] = title
        if duration and isinstance(duration, int):
            payload["duration"] = duration
        if fontsize and fontsize in self.FONTSIZES:
            payload["fontsize"] = self.FONTSIZES.get(fontsize)
        if position and position in self.POSITIONS:
            payload["position"] = self.POSITIONS.get(position)
        if bkgcolor and bkgcolor in self.BKG_COLORS:
            payload["bkgcolor"] = self.BKG_COLORS.get(bkgcolor)
        if transparency and transparency in self.TRANSPARENCIES:
            payload["transparency"] = self.TRANSPARENCIES.get(transparency)
        if interrupt:
            payload["interrupt"] = 1
        if icon:
            payload["filename"] = (
                "image",
                image_file,
                "application/octet-stream",
                {"Expires": "0"},
            )
        if image_file:
            payload["filename2"] = (
                "image",
                image_file,
                "application/octet-stream",
                {"Expires": "0"},
            )

        try:
            _LOGGER.debug("Payload: %s", str(payload))
            response = requests.post(
                self.url, files=payload, timeout=self.DEFAULT_TIMEOUT
            )
            if response.status_code != 200:
                _LOGGER.error("Error sending message: %s", str(response))
                return False
        except (ConnectionError, ConnectTimeout) as err:
            _LOGGER.error("Error communicating with %s: %s", self.url, str(err))
            raise ConnectError from err
        return True

class ConnectError(Exception):
    """Exception raised for connection error."""
