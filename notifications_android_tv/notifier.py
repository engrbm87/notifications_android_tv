"""Notification class for Android TV."""

import base64
import logging
from typing import Any

import httpx

from .const import (
    DEFAULT_ICON,
    DEFAULT_TITLE,
)
from .exceptions import ConnectError, InvalidResponse
from .helpers import NotificationParams

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
        httpx_client: httpx.AsyncClient = self.httpx_client or httpx.AsyncClient(
            verify=False
        )
        try:
            async with httpx_client as client:
                await client.get(self.url, timeout=30)
        except (httpx.ConnectError, httpx.TimeoutException) as err:
            raise ConnectError(f"Connection to {self.url} failed: {err}") from err

    async def async_send(
        self,
        message: str,
        *,
        title: str | None = None,
        params: NotificationParams | None = None,
    ) -> None:
        """Send message with parameters.

        :param message: The notification message.
        :param title: (Optional) The notification title.
        :params params: (Optional) Notification parameters. Construct using NotificationParams.

        Usage:
        >>> from notifications_android_tv import Notifications
        >>> notifier = Notifications("192.168.3.88")
        >>> await notifier.async_connect()
        >>> await notifier.async_send(
                "message to be sent",
                title="Notification title",
                params=NotificationParams(
                    duration=5,
                    position=Positions.BOTTOM_RIGHT,
                    fontsize=FontSize.MEDIUM,
                )
            )
        """
        data: dict[str, Any] = {
            "msg": message,
            "title": title or DEFAULT_TITLE,
        }
        if params is not None:
            data.update(params.data_params)
            files = await params.get_images()
        else:
            icon_bytes = base64.b64decode(DEFAULT_ICON)
            files = {
                "filename": (
                    "image",
                    icon_bytes,
                    "application/octet-stream",
                    {"Expires": "0"},
                )
            }

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
