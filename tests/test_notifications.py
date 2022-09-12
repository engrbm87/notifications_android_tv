"""Tests for Notifications."""
import pytest
from notifications_android_tv import Notifications, ConnectError, BKG_COLORS

@pytest.mark.asyncio
async def test_connection_fails():
    """Test connecting to the TV fails."""

    notifier = Notifications('192.168.3.88')
    with pytest.raises(ConnectError):
        await notifier.async_connect()

@pytest.mark.asyncio
async def test_connection_successful():
    """Test connecting to the TV."""

    notifier = Notifications('192.168.88.29')
    await notifier.async_connect()

@pytest.mark.asyncio
async def test_sending_message():
    """Test connecting to the TV."""

    notifier = Notifications('192.168.3.88')
    with open("rami.jpg", "rb") as file: 
        image = file.read()
        await notifier.async_send(
            "Hello1",
            title="Title",
            bkgcolor="red",
            icon=image,
            image_file=image
        )