"""Example scripts for sending notifications."""

import asyncio
import logging

from notifications_android_tv import ConnectError, Notifications
from notifications_android_tv.exceptions import NotificationException
from notifications_android_tv.notifier import NotificationParams

_LOGGER = logging.getLogger(__name__)

HOST = "<host>"
ICON = "<icon path or url>"
IMAGE = "<image path or url>"


async def main() -> None:
    """Run the example script."""
    notifier = Notifications(HOST)

    # validate connection
    try:
        await notifier.async_connect()
    except ConnectError as err:
        _LOGGER.error(err)
        return

    # # Send a basic notification with message only
    await notifier.async_send("This is a simple notification message")

    # For constructing paramters from string values as documented
    # in Home Assistant https://www.home-assistant.io/integrations/nfandroidtv
    notification_params = NotificationParams.from_dict(
        {
            "duration": "10",
            "color": "red",
            "fontsize": "small",
            "position": "bottom-right",
            "transparency": "25%",
            "interrupt": 0,
            "icon": {"path": ICON},
            "image": {"url": IMAGE},
        }
    )
    try:
        await notifier.async_send(
            "This is a notification message",
            title="Notification Title",
            params=notification_params,
        )
    except NotificationException as err:
        _LOGGER.error(err)


if __name__ == "__main__":
    asyncio.run(main())
