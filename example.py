"""Example scripts for sending notifications."""
import asyncio
from typing import Any

from notifications_android_tv import (
    BkgColors,
    ConnectError,
    FontSizes,
    ImageUrlSource,
    Notifications,
    Positions,
    Transparencies,
)

HOST = "127.0.0.1"
IMAGE_SOURCE = "<replace with url link or file path>"


async def main() -> None:
    """Run the example script."""
    notifier = Notifications(HOST)

    # validate connection
    try:
        await notifier.async_connect()
    except ConnectError:
        return

    # Send a basic notification with message only
    await notifier.async_send("This is a notification message")

    # Customize all paramters in the notification
    await notifier.async_send(
        "This is a notification message",
        title="Notification Title",
        duration=5,
        bkgcolor=BkgColors.RED,
        fontsize=FontSizes.LARGE,
        position=Positions.CENTER,
        transparency=Transparencies._75_PERCENT,
        interrupt=True,
        icon=ImageUrlSource(IMAGE_SOURCE),
        image_file=ImageUrlSource(IMAGE_SOURCE),
    )

    # For constructing paramters from string values as documented
    # in Home Assistant https://www.home-assistant.io/integrations/nfandroidtv
    data: dict[str, Any] = {
        "duration": 5,
        "color": "red",
        "fontsize": "medium",
        "position": "bottom-right",
        "transparency": "75%",
        "interrupt": 0,
        "icon": {"url": "<image url>"},
        "image": {"url": "<image url>"},
    }

    await notifier.async_send(
        "This is a notification message",
        title="Notification Title",
        duration=int(data["duration"]),
        bkgcolor=BkgColors[data["color"].upper()],
        fontsize=FontSizes[data["fontsize"].upper()],
        position=Positions[data["position"].upper().replace("-", "_")],
        transparency=Transparencies[f"{data['transparency'].replace('%', '_PERCENT')}"],
        interrupt=data["interrupt"],
        icon=ImageUrlSource(data["icon"]),
        image_file=ImageUrlSource(data["image"]),
    )


if __name__ == "__main__":
    asyncio.run(main())
