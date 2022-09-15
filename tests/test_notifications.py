"""Tests for Notifications."""

import httpx
import pytest
from pytest_httpx import HTTPXMock

from notifications_android_tv import ImageUrlSource, Notifications, exceptions


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


@pytest.mark.asyncio
async def test_get_image_fails(httpx_mock: HTTPXMock) -> None:
    """Test getting an image from source fails."""
    notifier = Notifications("0.0.0.0")

    # test getting image non existing file fails
    with pytest.raises(exceptions.InvalidImage):
        await notifier.async_send("Message text", icon="image_file.jpg")

    # test image url doesn't return 200
    httpx_mock.add_response(status_code=400)
    with pytest.raises(exceptions.InvalidImage):
        await notifier.async_send(
            "Message text", icon=ImageUrlSource("http://example.com/image.png")
        )

    # test returned content is not an image type
    httpx_mock.add_response(headers={"content-type": "text/html"})
    with pytest.raises(exceptions.InvalidImage):
        await notifier.async_send(
            "Message text", icon=ImageUrlSource("http://example.com")
        )


@pytest.mark.asyncio
async def test_image_source() -> None:
    """Test constructing ImageUrlSource."""
    # test provding wrong authentication type
    with pytest.raises(ValueError) as err:
        ImageUrlSource("http://example.com/image.png", auth="something")
        assert err == "authentication must be 'basic' or 'digest'"

    # test missing password
    with pytest.raises(ValueError) as err:
        ImageUrlSource("http://example.com/image.png", auth="basic", username="user")
        assert err == "username and password must be specified"

    # test missing username
    with pytest.raises(ValueError) as err:
        ImageUrlSource("http://example.com/image.png", auth="basic", password="pass")
        assert err == "username and password must be specified"

    # test providing image source from dict
    image_source_dict = {
        "url": "http://example.com/image.png",
        "auth": "basic",
        "username": "user",
        "password": "pass",
    }
    image_source = ImageUrlSource(**image_source_dict)
    assert image_source.url == "http://example.com/image.png"
    assert type(image_source._auth) is httpx.BasicAuth
