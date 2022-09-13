"""Tests for Notifications."""
import httpx
import pytest
from pytest_httpx import HTTPXMock

from notifications_android_tv import Notifications, exceptions


@pytest.mark.asyncio
async def test_timeout(httpx_mock: HTTPXMock) -> None:
    """Test if the connection is hitting the timeout."""

    def raise_timeout(request):
        """Set the timeout for the requests."""
        raise httpx.ReadTimeout(
            f"Unable to read within {request.extensions['timeout']}", request=request
        )

    httpx_mock.add_callback(raise_timeout)

    with pytest.raises(exceptions.ConnectError):
        notifier = Notifications("0.0.0.0")
        await notifier.async_connect()


@pytest.mark.asyncio
async def test_sending_failed(httpx_mock: HTTPXMock) -> None:
    """Test sending a message fails."""
    httpx_mock.add_response(status_code=400)

    notifier = Notifications("0.0.0.0")
    with pytest.raises(exceptions.InvalidResponse):
        await notifier.async_send("Message text")


@pytest.mark.asyncio
async def test_sending_successfull(httpx_mock: HTTPXMock) -> None:
    """Test sending a message is successful."""
    httpx_mock.add_response(status_code=200)

    notifier = Notifications("0.0.0.0")
    await notifier.async_send("Message text")
