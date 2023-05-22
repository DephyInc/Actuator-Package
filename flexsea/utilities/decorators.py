from functools import wraps
from typing import Any, Callable

from semantic_version import Version


# ============================================
#              requires_status
# ============================================
def requires_status(status) -> Callable:
    """
    Ensures we are either connected or streaming.
    """

    def status_decorator(func: Callable) -> Callable:
        @wraps(func)
        def status_wrapper(*args, **kwargs) -> Any:
            if not getattr(args[0], status):
                raise RuntimeError(f"Error: not {status}.")
            return func(*args, **kwargs)

        return status_wrapper

    return status_decorator


# ============================================
#                  validate
# ============================================
def validate(func) -> Callable:
    """
    Checks if the result of a command is SUCCESS.
    """

    @wraps(func)
    def validate_wrapper(*args, **kwargs) -> Any:
        retCode = func(*args, **kwargs)
        # pylint: disable-next=protected-access
        if retCode != args[0]._SUCCESS.value:
            raise RuntimeError(f"Command: {func.__name__} failed.")
        return retCode

    return validate_wrapper


# ============================================
#           minimum_required_version
# ============================================
def minimum_required_version(version: str) -> Callable:
    """
    Makes sure that the device's firmware is at least the given
    version.
    """

    def min_ver_decorator(func: Callable) -> Callable:
        @wraps(func)
        def min_ver_wrapper(*args, **kwargs) -> Any:
            try:
                deviceVersion = args[0].firmwareVersion
            except AttributeError as err:
                raise RuntimeError("Must decorate a device method.") from err

            try:
                assert deviceVersion >= Version(version)
            except AssertionError as err:
                msg = f"Cannot use: {func.__name__}, firmware too low."
                raise RuntimeError(msg) from err
            return func(*args, **kwargs)

        return min_ver_wrapper

    return min_ver_decorator
