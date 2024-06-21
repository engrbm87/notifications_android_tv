"""Exceptions raised by the library."""


class NotificationException(Exception):
    """Base class for all exceptions raised by the library."""


class ConnectError(NotificationException):
    """Exception raised for connection error."""


class InvalidResponse(NotificationException):
    """Exception raised for invalid response."""


class InvalidImage(NotificationException):
    """Exception raised for invalid image."""
