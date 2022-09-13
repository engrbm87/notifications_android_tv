"""Library for sending notifications to Android/Fire TVs."""

from __future__ import annotations

import base64
from io import BufferedReader, BytesIO
import logging
from typing import Any

import httpx

from .const import BKG_COLORS, DEFAULT_ICON, FONTSIZES, POSITIONS, TRANSPARENCIES
from .exceptions import ConnectError, InvalidResponse

_LOGGER = logging.getLogger(__name__)


class Notifications:
    """Notifications class for Android/Fire Tvs."""

    def __init__(
        self,
        host: str,
        port: int = 7676,
        httpx_client: httpx.AsyncClient | None = None,
    ) -> None:
        """Initialize notifier."""
        self.url = f"http://{host}:{port}"
        self.httpx_client = httpx_client

    async def async_connect(self) -> None:
        """Test connecting to server."""
        httpx_client: httpx.AsyncClient = (
            self.httpx_client if self.httpx_client else httpx.AsyncClient(verify=False)
        )
        try:
            async with httpx_client as client:
                await client.get(self.url, timeout=5)
        except (httpx.ConnectError, httpx.TimeoutException) as err:
            raise ConnectError(f"Connection to {self.url} failed") from err

    async def async_send(
        self,
        message: str,
        title: str | None = None,
        duration: int | None = None,
        fontsize: str | None = None,
        position: str | None = None,
        bkgcolor: str | None = None,
        transparency: str | None = None,
        interrupt: bool = False,
        icon: BufferedReader | bytes | None = None,
        image_file: BufferedReader | bytes | None = None,
    ) -> None:
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

        Usage:
        >>> from notifications_android_tv import Notifications
        >>> notifier = Notifications("192.168.3.88")
        >>> notifier.async_send(
                "message to be sent",
                title="Notification title",
                duration="20",
                transparency="100%"
            )
        """
        data: dict[str, Any] = {
            "msg": message,
        }
        if title:
            data["title"] = title
        if duration:
            data["duration"] = duration
        if fontsize in FONTSIZES:
            data["fontsize"] = FONTSIZES[fontsize]
        if position in POSITIONS:
            data["position"] = POSITIONS[position]
        if bkgcolor in BKG_COLORS:
            data["bkgcolor"] = BKG_COLORS[bkgcolor]
        if transparency in TRANSPARENCIES:
            data["transparency"] = TRANSPARENCIES[transparency]
        if interrupt:
            data["interrupt"] = 1

        files = {
            "filename": (
                "image",
                icon or BytesIO(base64.b64decode(DEFAULT_ICON)),
                "application/octet-stream",
                {"Expires": "0"},
            )
        }
        if image_file:
            files["filename2"] = (
                "image",
                image_file,
                "application/octet-stream",
                {"Expires": "0"},
            )
        _LOGGER.info("data: %s, files: %s", data, files)

        httpx_client: httpx.AsyncClient = (
            self.httpx_client if self.httpx_client else httpx.AsyncClient(verify=False)
        )
        try:
            async with httpx_client as client:
                response = await client.post(
                    self.url, data=data, files=files, timeout=5
                )

        except (httpx.ConnectError, httpx.TimeoutException) as err:
            raise ConnectError(f"Error communicating with {self.url}: {err}") from err
        if response.status_code != httpx.codes.OK:
            raise InvalidResponse(f"Error sending message: {response}")
