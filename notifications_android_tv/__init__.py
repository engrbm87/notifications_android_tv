"""Library for sending notifications to Android/Fire TVs."""

from __future__ import annotations

import base64
import logging
from typing import Any

import httpx

from .const import (
    DEFAULT_ICON,
    DEFAULT_TITLE,
    BkgColors,
    FontSizes,
    Positions,
    Transparencies,
)
from .exceptions import ConnectError, InvalidImage, InvalidResponse

_LOGGER = logging.getLogger(__name__)


class ImageUrlSource:
    """Image source from url or local path."""

    def __init__(
        self,
        url: str,
        username: str | None = None,
        password: str | None = None,
        auth: str | None = None,
    ) -> None:
        """Initiate image source class."""
        self.url = url
        self.auth: httpx.Auth | None = None

        if auth:
            if auth not in ["basic", "digest"]:
                raise ValueError("authentication must be 'basic' or 'digest'")
            if username is None or password is None:
                raise ValueError("username and password must be specified")
            if auth == "basic":
                self.auth = httpx.BasicAuth(username, password)
            else:
                self.auth = httpx.DigestAuth(username, password)


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

    async def _async_get_image(self, image_source: ImageUrlSource | str) -> bytes:
        """Load file from path or url."""
        httpx_client: httpx.AsyncClient = self.httpx_client or httpx.AsyncClient(
            verify=False
        )
        if isinstance(image_source, ImageUrlSource):
            try:
                async with httpx_client as client:
                    response = await client.get(
                        image_source.url, auth=image_source.auth, timeout=30
                    )

            except (httpx.ConnectError, httpx.TimeoutException) as err:
                raise ConnectError(
                    f"Error fetching image from {image_source.url}: {err}"
                ) from err
            if response.status_code != httpx.codes.OK:
                raise InvalidImage(
                    f"Error fetching image from {image_source.url}: {response}"
                )
            if "image" not in response.headers["content-type"]:
                raise InvalidImage(
                    f"Response content type is not an image: {response.headers['content-type']}"
                )
            return response.content
        try:
            with open(image_source, "rb") as file:
                image = file.read()
        except FileNotFoundError as err:
            raise InvalidImage(err) from err
        return image

    async def async_connect(self) -> None:
        """Test connecting to server."""
        httpx_client: httpx.AsyncClient = self.httpx_client or httpx.AsyncClient(
            verify=False
        )
        try:
            async with httpx_client as client:
                await client.get(self.url, timeout=5)
        except (httpx.ConnectError, httpx.TimeoutException) as err:
            raise ConnectError(f"Connection to {self.url} failed") from err

    async def async_send(
        self,
        message: str,
        title: str = DEFAULT_TITLE,
        duration: int = 5,
        bkgcolor: BkgColors = BkgColors.GREY,
        fontsize: FontSizes = FontSizes.MEDIUM,
        position: Positions = Positions.BOTTOM_RIGHT,
        transparency: int = Transparencies.from_percentage("0%"),
        interrupt: bool = False,
        icon: ImageUrlSource | str | None = None,
        image_file: ImageUrlSource | str | None = None,
    ) -> None:
        """Send message with parameters.

        :param message: The notification message.
        :param title: (Optional) The notification title.
        :param duration: (Optional) Display the notification for the specified period.
            Default duration is 5 seconds.
        :param fontsize: (Optional) Specify text font size from class `Fontsizes`.
            Default is `FontSizes.MEDIUM`.
        :param position: (Optional) Specify notification position from class `Positions`.
            Default is `Positions.BOTTOM_RIGHT`.
        :param bkgcolor: (Optional) Specify background color from class BkgColors.
            Default is `BkgColors.GREY`.
        :param transparency: (Optional) Specify the background transparency of the notification
            from class `Transparencies`. Default is `Transparencies._0_PERCENT`.
        :param interrupt: (Optional) Setting it to true makes the notification interactive
            and can be dismissed or selected to display more details. Default is False
        :param icon: (Optional) Attach icon to notification. Type must be `bytes`.
        :param image_file: (Optional) Attach image to notification. Type must be `bytes`.

        Usage:
        >>> from notifications_android_tv import Notifications
        >>> notifier = Notifications("192.168.3.88")
        >>> await notifier.async_connect()
        >>> await notifier.async_send(
                "message to be sent",
                title="Notification title",
                duration="20",
                transparency="100%"
            )
        """
        data: dict[str, Any] = {
            "msg": message,
            "title": title,
            "duration": duration,
            "bkgcolor": bkgcolor.value,
            "fontsize": fontsize.value,
            "position": position.value,
            "transparency": transparency,
            "interrupt": interrupt,
        }

        icon_bytes = base64.b64decode(DEFAULT_ICON)
        if icon is not None:
            try:
                icon_bytes = await self._async_get_image(icon)
            except InvalidImage as err:
                _LOGGER.warning(err)

        files = {
            "filename": (
                "image",
                icon_bytes,
                "application/octet-stream",
                {"Expires": "0"},
            )
        }
        if image_file:
            try:
                image_bytes = await self._async_get_image(image_file)
            except InvalidImage as err:
                _LOGGER.warning(err)
            else:
                files["filename2"] = (
                    "image",
                    image_bytes,
                    "application/octet-stream",
                    {"Expires": "0"},
                )
        _LOGGER.debug("data: %s, files: %s", data, files)

        httpx_client: httpx.AsyncClient = self.httpx_client or httpx.AsyncClient(
            verify=False
        )
        try:
            async with httpx_client as client:
                response = await client.post(
                    self.url, data=data, files=files, timeout=10
                )

        except (httpx.ConnectError, httpx.TimeoutException) as err:
            raise ConnectError(f"Error communicating with {self.url}: {err}") from err
        if response.status_code != httpx.codes.OK:
            raise InvalidResponse(f"Error sending message: {response}")
