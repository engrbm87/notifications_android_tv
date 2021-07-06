# Android TV / Fire TV Notifications

Python package that interfaces with Notifications for Android TV and Notifications for Fire TV to send notifications to your TV.

## Usage

```python
from notifications_android_tv import Notifier
notify = Notifier("192.168.1.10")
notify.send("message")
```

## Optional parameters

- `title`: Notification title
- `duration`: Display the notification for the specified period. Default is 5 seconds
- `fontsize`: Text font size. Can be one of (`small`, `medium`, `large`, `max`)
- `position`: Notification position. Can be one of (`bottom-right`, `bottom-left`, `top-right`, `top-left`, `center`). Default is `bottom-right`.
- `bkgcolor`: Notification background color. Can be one of (`grey`, `black`, `indigo`, `green`, `red`, `cyan`, `teal`, `amber`, `pink`). Default is `grey`.
- `transparency`: Background transparency of the notification. Can be one of (`0%`, `25%`, `50%`, `75%`, `100%`). Default is `0%`.
- `interrupt`: Setting it to `True` makes the notification interactive and can be dismissed or selected to display more details. Default is `False`
- `icon`: Attach icon to notification. Type must be `bytes`.
- `image_file`: Attach image to notification. Type must be `bytes`.
