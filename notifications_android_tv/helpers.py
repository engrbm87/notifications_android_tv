"""Helper methods for the library."""

from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Any

import httpx

from .const import (
    DEFAULT_BKGCOLOR,
    DEFAULT_DURATION,
    DEFAULT_FONTSIZE,
    DEFAULT_ICON,
    DEFAULT_POSITION,
    DEFAULT_TRANSPARENCY,
    BkgColor,
    FontSize,
    Position,
    Transparency,
)
from .exceptions import ConnectError, InvalidImage


@dataclass
class ImageSource:
    """Image source from url or local path."""

    path: str | None = None
    url: str | None = None
    auth: httpx.Auth | None = None

    @classmethod
    def from_path(cls, path: str) -> ImageSource:
        """Initiate image source class."""

        return cls(path=path)

    @classmethod
    def from_url(
        cls,
        url: str | None = None,
        username: str | None = None,
        password: str | None = None,
        auth: str | None = None,
    ) -> ImageSource:
        """Initiate image source class."""
        _cls = cls(url=url)
        if auth:
            if auth not in ["basic", "digest"]:
                raise ValueError("authentication must be 'basic' or 'digest'")
            if username is None or password is None:
                raise ValueError("username and password must be specified")
            if auth == "basic":
                _cls.auth = httpx.BasicAuth(username, password)
            else:
                _cls.auth = httpx.DigestAuth(username, password)

        return _cls

    async def async_get_image(self) -> bytes:
        """Load file from path or url."""
        if self.path is not None:
            try:
                with open(self.path, "rb") as file:
                    return file.read()
            except FileNotFoundError as err:
                raise InvalidImage(err) from err
        if self.url is not None:
            try:
                async with httpx.AsyncClient(verify=False) as client:
                    response = await client.get(self.url, auth=self.auth, timeout=30)

            except (httpx.ConnectError, httpx.TimeoutException) as err:
                raise ConnectError(
                    f"Error fetching image from {self.url}: {err}"
                ) from err
            if response.status_code != httpx.codes.OK:
                raise InvalidImage(f"Error fetching image from {self.url}: {response}")
            if "image" not in response.headers["content-type"]:
                raise InvalidImage(
                    f"Response content type is not an image: {response.headers['content-type']}"
                )
            return response.content
        raise ValueError("Either path or url must be specified")


@dataclass
class NotificationParams:
    """Notification parameters.

    :param duration: (Optional) Display the notification for the specified period.
        Default duration is 5 seconds.
    :param position: (Optional) Specify notification position from class Position.
        Default is `Positions.BOTTOM_RIGHT`.
    :param fontsize: (Optional) Specify text font size from class FontSize.
        Default is `FontSizes.MEDIUM`.
    :param color: (Optional) Specify background color from class BkgColor.
        Default is `BkgColors.GREY`.
    :param transparency: (Optional) Specify the background transparency of the notification
        from class `Transparency`. Default is 0%.
    :param interrupt: (Optional) Setting it to true makes the notification interactive
        and can be dismissed or selected to display more details. Default is False
    :param icon: (Optional) Attach icon to notification. Construct using ImageSource.
    :param image_file: (Optional) Attach image to notification. Construct using ImageSource.
    """

    duration: int = DEFAULT_DURATION
    position: int = DEFAULT_POSITION
    fontsize: FontSize = DEFAULT_FONTSIZE
    transparency: int = DEFAULT_TRANSPARENCY
    color: BkgColor = DEFAULT_BKGCOLOR
    interrupt: bool = False
    icon: ImageSource | None = None
    image: ImageSource | None = None

    @property
    def data_params(self) -> dict[str, Any]:
        """Return notification parameters as a dict."""
        return {
            "duration": self.duration,
            "position": self.position,
            "fontsize": self.fontsize.value,
            "transparency": self.transparency,
            "color": self.color.value,
            "interrupt": self.interrupt,
        }

    async def get_images(self) -> dict[str, Any]:
        """Return notification icon and image."""
        icon_bytes = base64.b64decode(DEFAULT_ICON)
        if self.icon is not None:
            icon_bytes = await self.icon.async_get_image()
        files = {
            "filename": (
                "image",
                icon_bytes,
                "application/octet-stream",
                {"Expires": "0"},
            )
        }
        if self.image is not None:
            image_bytes = await self.image.async_get_image()
            files["filename2"] = (
                "image",
                image_bytes,
                "application/octet-stream",
                {"Expires": "0"},
            )
        return files

    @classmethod
    def from_dict(cls, kwargs: dict[str, Any]) -> NotificationParams:
        """Initiate notification parameters class."""
        _params: dict[str, Any] = {}
        if duration := kwargs.get("duration"):
            try:
                _params["duration"] = int(duration)
            except ValueError:
                _params["duration"] = DEFAULT_DURATION

        if position := kwargs.get("position"):
            _params["position"] = Position.from_string(position)

        if (font_size := kwargs.get("fontsize")) and hasattr(
            FontSize, font_size.upper()
        ):
            _params["fontsize"] = getattr(FontSize, font_size.upper())

        if transparency := kwargs.get("transparency"):
            _params["transparency"] = Transparency.from_percentage(transparency)

        if (color := kwargs.get("color")) and hasattr(BkgColor, color.upper()):
            _params["color"] = getattr(BkgColor, color.upper())

        if interrupt := kwargs.get("interrupt"):
            _params["interrupt"] = bool(interrupt)

        if icon := kwargs.get("icon"):
            if isinstance(icon, str):
                _params["icon"] = (
                    ImageSource.from_url(icon)
                    if icon.startswith("http")
                    else ImageSource.from_path(icon)
                )
            elif isinstance(icon, dict) and "path" in icon:
                _params["icon"] = ImageSource.from_path(icon["path"])
            elif isinstance(icon, dict) and "url" in icon:
                _params["icon"] = ImageSource.from_url(**icon)

        if image := kwargs.get("image"):
            if isinstance(image, str):
                _params["image"] = (
                    ImageSource.from_url(image)
                    if image.startswith("http")
                    else ImageSource.from_path(image)
                )
            elif isinstance(image, dict) and "path" in image:
                _params["image"] = ImageSource.from_path(image["path"])
            elif isinstance(image, dict) and "url" in image:
                _params["image"] = ImageSource.from_url(**image)

        return NotificationParams(**_params)
