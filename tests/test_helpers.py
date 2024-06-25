"""Tests for helper classes."""

import httpx
import pytest
from pytest_httpx import HTTPXMock

from notifications_android_tv import ImageSource
from notifications_android_tv import ConnectError, InvalidImage


@pytest.mark.asyncio
async def test_image_source() -> None:
    """Test constructing ImageSource."""
    # test provding wrong authentication type
    with pytest.raises(ValueError) as err:
        ImageSource.from_url(url="http://example.com/image.png", auth="something")
        assert err == "authentication must be 'basic' or 'digest'"

    # test missing password
    with pytest.raises(ValueError) as err:
        ImageSource.from_url(
            url="http://example.com/image.png", auth="basic", username="user"
        )
        assert err == "username and password must be specified"

    # test missing username
    with pytest.raises(ValueError) as err:
        ImageSource.from_url(
            "http://example.com/image.png", auth="basic", password="pass"
        )
        assert err == "username and password must be specified"

    # test url with basic auth
    image_source_dict = {
        "url": "http://example.com/image.png",
        "auth": "basic",
        "username": "user",
        "password": "pass",
    }
    image_source = ImageSource.from_url(**image_source_dict)
    assert image_source.url == "http://example.com/image.png"
    assert isinstance(image_source.auth, httpx.BasicAuth)

    # test url with digest auth
    image_source_dict = {
        "url": "http://example.com/image.png",
        "auth": "digest",
        "username": "user",
        "password": "pass",
    }
    image_source = ImageSource.from_url(**image_source_dict)
    assert image_source.url == "http://example.com/image.png"
    assert isinstance(image_source.auth, httpx.DigestAuth)


@pytest.mark.asyncio
async def test_get_image_fails(httpx_mock: HTTPXMock) -> None:
    """Test getting an image from source fails."""
    image = ImageSource.from_url(url="http://example.com")

    # test timeout fetching image
    with pytest.raises(ConnectError):
        httpx_mock.add_exception(httpx.TimeoutException(""))
        await image.async_get_image()

    # test image url doesn't return 200
    httpx_mock.add_response(status_code=400)
    with pytest.raises(InvalidImage):
        await image.async_get_image()

    # test returned content is not an image type
    httpx_mock.add_response(headers={"content-type": "text/html"})
    with pytest.raises(InvalidImage):
        await image.async_get_image()

    # test getting image non existing file fails
    image2 = ImageSource.from_path("image_file.jpg")
    with pytest.raises(InvalidImage):
        await image2.async_get_image()
