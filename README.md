# Android TV / Fire TV Notifications

Python package that interfaces with [Notifications for Android TV](https://play.google.com/store/apps/details?id=de.cyberdream.androidtv.notifications.google) and [Notifications for Fire TV](https://play.google.com/store/apps/details?id=de.cyberdream.firenotifications.google) to send notifications to your TV.

## Usage

- Install the application on your TV
- Get the IP of the TV unit

```python
from notifications_android_tv import Notifications
notify = Notifications("192.168.1.10")
# validate connection
try:
    await notify.async_connect()
expect ConnectError:
    return False
await notify.async_send(
    "message text",
    title="Title text",
)
```

## Optional parameters

- `title`: Notification title
- `duration`: Display the notification for the specified period. Default is 5 seconds
- `fontsize`: Text font size. Use `FontSizes` class to set the fontsize. Default is `FontSizes.MEDIUM`
- `position`: Notification position. Use `Positions` class to set position. Default is `Positions.BOTTOM_RIGHT`.
- `bkgcolor`: Notification background color. Use `BkgColors` class to set color. Default is `BkgColors.GREY`.
- `transparency`: Background transparency of the notification. Use `Transparencies` class. Default is `Transparencies._0_PERCENT`.
- `interrupt`: Setting it to `True` makes the notification interactive and can be dismissed or selected to display more details. Default is `False`
- `icon`: Can be `str` represnting the file path or an `ImageUrlSource` that includes the url and authentication params to fetch the image from a url.
- `image_file`: Can be `str` represnting the file path or an `ImageUrlSource` that includes the url and authentication params to fetch the image from a url.

Refer to the [example file](example.py) for setting these parameters directly or from a data dictionary (as documented in <https://www.home-assistant.io/integrations/nfandroidtv>)
