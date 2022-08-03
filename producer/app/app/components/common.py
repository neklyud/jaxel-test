"""Common classes and functions for using in producer microservice."""


from typing import Any, Dict


class Singleton(type):
    """Singleton metaclass."""

    _instances: Dict[Any, Any] = {}

    def __call__(cls, *args, **kwargs):
        """Initialize singleton object."""
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(
                *args, **kwargs,
            )
        return cls._instances[cls]
