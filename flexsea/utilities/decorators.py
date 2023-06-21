from functools import wraps
from typing import Any, Callable

from botocore.exceptions import ClientError
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


# ============================================
#             check_status_code
# ============================================
def check_status_code(func: Callable) -> Callable:
    @wraps(func)
    def check_status_wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        # boto3 raises a client error when we either try to download something
        # that doesn't exist, download something we don't have permission for,
        # or try to list the contents of a bucket when we don't have the
        # credentials to do so. These errors are differentiated by the
        # HTTPStatusCode key in the response
        except ClientError as err:
            statusCode = err.response["ResponseMetadata"]["HTTPStatusCode"]
            if statusCode == 404:
                msg = "Error: requested object could not be found on S3. "
                msg += "Please check spelling and/or path."
            elif statusCode == 403:
                msg = "Error: S3 permission denied. Please check your credentials "
                msg += "in '~/.aws/credentials' and make sure you're passing the "
                msg += "correct profile to the function."
            else:
                msg = f"Error: received status code {statusCode} from S3."
            raise RuntimeError(msg) from err

    return check_status_wrapper