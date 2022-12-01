import ctypes as c
import hashlib
import os
from pathlib import Path
import platform
import sys

import boto3
import botocore.exceptions as bce
from flexsea.specs.api_spec import apiSpec

from . import config as cfg


# ============================================
#                   get_os
# ============================================
def get_os() -> str:
    """
    Returns the operating system and "bitness":

        * windows_32bit
        * windows_64bit
        * pi_32bit
        * pi_64bit
        * linux_32bit
        * linux_64bit

    Returns
    -------
    os : str
        The name and "bitness" of the current operating system.
    """
    system = platform.system().lower()

    if system == "linux":
        machine = os.uname().machine
        if machine.startswith("arm") or machine.startswith("aarch"):
            system = "pi"

    return system + "_" + platform.architecture()[0]


# ============================================
#                    decode
# ============================================
def decode(val: int) -> str:
    """
    Returns decoded version number formatted as x.y.z
    """
    major: int = 0
    minor: int = 0
    bug: int = 0

    if val > 0:
        while val % 2 == 0:
            major += 1
            val /= 2

        while val % 3 == 0:
            minor += 1
            val /= 3

        while val % 5 == 0:
            bug += 1
            val /= 5

    return f"{major}.{minor}.{bug}"


# ============================================
#                  load_clib
# ============================================
def load_clib(cLibVersion: str) -> c.CDLL:
    """
    Uses `ctypes` to load the appropriate C libraries depending on the
    OS.

    Parameters
    ----------
    cLibVersion : str
        The version of the pre-compiled libraries to use. The major
        version should match the major version of the firmware on the
        device. If no libraries are found, then we download them from
        AWS.

    Raises
    ------
    OSError:
        Raised if the precompiled libraries fail to load.

    Returns
    -------
    clib : ctypes.cdll.CDLL
        The Python object from which we can call the flexsea C
        functions.
    """
    _os = get_os()
    libDir = cfg.libsDir.joinpath(cLibVersion, _os)

    lib = cfg.windowsLib if "win" in _os else cfg.linuxLib
    libPath = libDir.joinpath(lib)

    if not libPath.exists():
        libDir.mkdir(parents=True, exist_ok=True)
        libObj = str(Path("libs").joinpath(cLibVersion, _os, lib).as_posix())

        download(cfg.libsBucket, libObj, str(libPath))

    if "win" in _os:
        try:
            for extraPath in os.environ["PATH"].split(";"):
                if os.path.exists(extraPath) and "mingw" in extraPath:
                    os.add_dll_directory(extraPath)
            os.add_dll_directory(libPath)
        except OSError:
            msg = f"Error loading precompiled library: `{libPath}`\n"
            msg += "The most likely cause is a mismatch between the Python, pip and "
            msg += "shell architectures.\nPlease ensure all three are either 32 or 64 "
            msg += "bit.\nKeep different versions isolated by virtual environments.\n"
            print(msg)
            sys.exit(1)

    clib = c.cdll.LoadLibrary(libPath)

    api = apiSpec[cLibVersion]

    for functionName, functionData in api.items():
        func = getattr(clib, functionData["name"], None)
        if func:
            func.argtypes = functionData["argtypes"]
            func.restype = functionData["returnType"]
        setattr(clib, functionName, func)

    return clib


# ============================================
#                  download
# ============================================
def download(fileobj: str, bucket: str, dest: str, profile: str | None = None) -> None:
    """
    Downloads `fileobj` from `bucket` to `dest` with the AWS
    credentials profile `profile`.

    Raises
    ------
    botocore.exceptions.ProfileNotFound
        If the given profile does not exist in the AWS credentials file.
        If the ~/.aws/credentials file does not exist.

    botocore.exceptions.PartialCredentialsError
        If the given profile is missing one or more required keys.

    AssertionError
        If the download fails.
    """
    try:
        session = boto3.Session(profile_name=profile)
    except bce.ProfileNotFound as err:
        raise err

    try:
        client = session.client("s3")
    except bce.PartialCredentialsError as err:
        raise err

    client.download_file(bucket, fileobj, dest)

    assert Path(dest).exists()

    # Check the local file's integrity by comparing its md5 hash to
    # AWS's md5 hash, called ETag
    objData = client.head_object(Bucket=bucket, Key=fileobj)
    awsHash = objData["ETag"].strip('"')

    with open(dest, "rb") as fd:
        data = fd.read()

    localHash = hashlib.md5(data).hexdigest()

    assert localHash == awsHash
