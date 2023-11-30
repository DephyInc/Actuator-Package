from functools import wraps
from typing import Any, Callable

from botocore.exceptions import ClientError
from semantic_version import Version


# ============================================
#              training_warn
# ============================================
def training_warn(func: Callable) -> Any:
    """
    Before training information is available or training commands can
    be sent, the device must finish its setup. The purpose of this
    wrapper is to provide a warning to the user if their command fails
    about why it probably failed and what they can do about it.

    Parameters
    ----------
    func : Callable
        The method being wrapped. Must be a training-specific method.

    Raises
    ------
    RuntimeError
        If the wrapped method does not return a SUCCESS status code.

    Returns
    -------
    Callable
        The wrapped method.
    """

    @wraps(func)
    def training_warn_wrapper(*args, **kwargs) -> Any:
        try:
            # The validate decorator runs the actual method and raises
            # a RuntimeError if the method was not successfull. This
            # try-except construction requires that the training_warn
            # decorator be used "on top" of validate
            retCode = func(*args, **kwargs)
        except RuntimeError as err:
            msg = f"Error: {func.__name__} failed. For training-specific methods, "
            msg += "1.) the device must be running off of battery power, 2.) "
            msg += "a Dephy controller must be present on the device, 3.) the device "
            msg += "must be ready to provide augmentation."
            raise RuntimeError(msg) from err
        return retCode

    return training_warn_wrapper


# ============================================
#            requires_device_not
# ============================================
def requires_device_not(device: str) -> Callable:
    """
    Certain ``Device`` class methods only work on non-Actpack devices.
    This meta-decorator ensures this.

    Parameters
    ----------
    device: str
        The type of device that the physical device **cannot** be.

    Raises
    ------
    RuntimeError
        If the physical device has type ``device``.

    Returns
    -------
    Callable
        The method being wrapped.
    """

    def not_device_decorator(func: Callable) -> Callable:
        @wraps(func)
        def not_device_wrapper(*args, **kwargs) -> Any:
            if getattr(args[0], "_name") == device:
                raise RuntimeError(f"Error: {func.__name__} does not work on {device}")
            return func(*args, **kwargs)

        return not_device_wrapper

    return not_device_decorator


# ============================================
#              requires_status
# ============================================
def requires_status(status: str) -> Callable:
    """
    Ensures we are either connected or streaming.

    Parameters
    ----------
    status : str
        The status to check for.

    Raises
    ------
    RuntimeError
        If the given status is not set.

    Returns
    -------
    Callable
        The method being wrapped.
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
def validate(func: Callable) -> Callable:
    """
    Checks if the result of a command is SUCCESS.

    Parameters
    ----------
    func : Callable
        The method being wrapped.

    Raises
    ------
    RuntimeError
        If the wrapped method does not return a SUCCESS status code.

    Returns
    -------
    Callable
        The wrapped method.
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

    Parameters
    ----------
    version : str
        The firmware version required in order to use the wrapped
        method.

    Raises
    ------
    RuntimeError
        If the wrapped method is not a :py:class:`Device` method or
        if the given version is greater than the device's firmware
        version.

    Returns
    -------
    Callable
        The wrapped method
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
    """
    Makes sure that the S3 request succeeded.

    Parameters
    ----------
    func : Callable
        The wrapped method.

    Raises
    ------
    RuntimeError
        If we receive a 403 (permission denied) or 404 (not found)
        status code.

    Returns
    -------
    Callable
        The wrapped method.
    """

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
