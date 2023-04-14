import concurrent.futures as cf
import ctypes as c
import hashlib
import os
import platform
import sys
from pathlib import Path
from time import sleep

import boto3
import botocore.exceptions as bce
from botocore.client import BaseClient
from botocore.handlers import disable_signing
from serial.tools.list_ports import comports

import flexsea.enums as fxe
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
            val = int(val / 2)

        while val % 3 == 0:
            minor += 1
            val = int(val / 3)

        while val % 5 == 0:
            bug += 1
            val = int(val / 5)

    return f"{major}.{minor}.{bug}"


# ============================================
#                  load_clib
# ============================================
def load_clib(
    cLibVersion: str, silent: bool = False, libFile: str | Path = ""
) -> c.CDLL:
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

    silent : bool (optional)
        If `True`, suppresses messages to stdout.

    libFile : str (optional)
        If set, specifies the library file to load. Overrides looking
        in the standard .dephy location and will not attempt to
        download the file if it isn't found. Still requires cLibVersion
        to know what api to use with the lib.

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

    if not libFile:
        lib = cfg.windowsLib if "win" in _os else cfg.linuxLib
        libFile = cfg.libsDir.joinpath(cLibVersion, _os, lib)

        if not libFile.exists():
            libFile.parent.mkdir(parents=True, exist_ok=True)
            libObj = str(Path("libs").joinpath(cLibVersion, _os, lib).as_posix())

            download(libObj, cfg.libsBucket, str(libFile))
    else:
        libFile = Path(libFile)

    if "win" in _os:
        try:
            for extraPath in os.environ["PATH"].split(";"):
                if os.path.exists(extraPath) and "mingw" in extraPath:
                    os.add_dll_directory(extraPath)
            os.add_dll_directory(str(libFile.parent.absolute()))
        except OSError:
            msg = f"Error loading precompiled library: `{libFile}`\n"
            msg += "The most likely cause is a mismatch between the Python, pip and "
            msg += "shell architectures.\nPlease ensure all three are either 32 or 64 "
            msg += "bit.\nKeep different versions isolated by virtual environments.\n"
            print(msg)
            sys.exit(1)

    clib = c.cdll.LoadLibrary(str(libFile.expanduser().absolute()))

    api = apiSpec[cLibVersion]

    for functionName, functionData in api["commands"].items():
        func = getattr(clib, functionData["name"], None)
        if func:
            func.argtypes = functionData["argTypes"]
            func.restype = functionData["returnType"]
        setattr(clib, functionName, func)

    if not silent:
        print(f"Using version: {cLibVersion} of pre-compiled C library.")
        print(f"Loading library from: {libFile}")

    return clib


# ============================================
#                  download
# ============================================
def download(fileObj: str, bucket: str, dest: str, profile: str | None = None) -> None:
    """
    Downloads `fileObj` from `bucket` to `dest` with the AWS
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

    if profile is None:
        resource = boto3.resource("s3")
        resource.meta.client.meta.events.register("choose-signer.s3.*", disable_signing)
        bucket = resource.Bucket(bucket)
        bucket.download_file(fileObj, dest)
    else:
        try:
            session = boto3.Session(profile_name=profile)
        except bce.ProfileNotFound as err:
            raise err

        try:
            client = session.client("s3")
        except bce.PartialCredentialsError as err:
            raise err

        client.download_file(bucket, fileObj, dest)
        # TODO(CA): Make validate download work when no profile is given
        _validate_download(client, bucket, fileObj, dest)


# ============================================
#             _validate_download
# ============================================
def _validate_download(
    client: BaseClient, bucket: str, fileObj: str, dest: str
) -> None:
    """
    Compares the AWS md5 hash to the local md5 hash to make sure the
    files are the same.

    S3 objects have an attribute called 'ETag', which is a string.
    There are two possibilities: the string is a hex digest or the
    string is a hex digest + -NUMBER.

    In the case that ETag has no -NUMBER suffix, it means that the ETag
    is the md5 hash of the file contents.

    In the case that there is a -NUMBER suffix, it means that the file
    was uploaded to S3 in NUMBER chunks and that the hex digest is actually
    the hex digest of the digests of all of the chunks concatenated together.

    Parameters
    ----------
    client : BaseClient
        The object that allows use to communicate with S3.

    bucket : str
        The name of the bucket the file came from.

    fileObj : str
        The name of the fileObj we are validating.

    dest : str
        The name of the dowloaded file on disk.
    """
    assert Path(dest).exists()

    # Check the local file's integrity by comparing its md5 hash to
    # AWS's md5 hash, called ETag
    objData = client.head_object(Bucket=bucket, Key=fileObj)
    etag = objData["ETag"].strip('"')

    try:
        nChunks = int(etag.split("-")[1])
    except IndexError:
        nChunks = 1

    if nChunks == 1:
        with open(dest, "rb") as fd:
            data = fd.read()
        localHash = hashlib.md5(data).hexdigest()

    elif nChunks > 1:
        chunkHashes = []
        with open(dest, "rb") as fd:
            for chunk in range(1, nChunks + 1):
                objData = client.head_object(
                    Bucket=bucket, Key=fileObj, PartNumber=chunk
                )
                chunkSize = objData["ContentLength"]
                data = fd.read(chunkSize)
                if data:
                    chunkHashes.append(hashlib.md5(data))
                else:
                    break

        if len(chunkHashes) == 1:
            localHash = chunkHashes[0].hexdigest()
        else:
            digests = b"".join([m.digest() for m in chunkHashes])
            digestsMd5 = hashlib.md5(digests)
            localHash = f"{digestsMd5.hexdigest()}-{len(chunkHashes)}"

    assert localHash == etag


# ============================================
#                   find_port
# ============================================
def find_port(baudRate: int, cLibVersion: str, libFile: str = "") -> str:
    """
    Tries to establish a connection to the Dephy device given by
    the user-supplied port. If no port is supplied, then we loop
    over all available serial ports to try and find a valid device.

    Parameters
    ----------
    baudRate : int
        Baud rate for communicating with the device.

    cLibVersion : str
        The semantic version string of the firmware currently on the device.

    libFile : str (optional)
        If set, specifies the library file to load. Overrides looking
        in the standard .dephy location and will not attempt to
        download the file if it isn't found. Still requires cLibVersion
        to know what api to use with the lib.


    Raises
    ------
    RuntimeError
        If no valid Dephy device can be found.

    Returns
    -------
    devicePort : str
        Name of the device's COM port.
    """
    devicePort = None
    successVals = [
        fxe.dephyDeviceErrorCodes["SUCCESS"].value,
        fxe.legacyDeviceErrorCodes["SUCCESS"].value,
    ]
    clib = load_clib(cLibVersion, True, libFile)

    for _port in comports():
        p = _port.device

        # Not using multiprocessing.Process b/c Windows doesn't support the "fork"
        # start method, only "spawn". Spawn cannot pickle a clib object and so the
        # code crashes
        with cf.ThreadPoolExecutor() as executor:
            future = executor.submit(_timed_open, clib, p, baudRate, 0)
            try:
                deviceId = future.result(timeout=10)
            except TimeoutError:
                continue
            devicePort = p
            sleep(0.1)
            retValue = clib.close(deviceId)
            if retValue not in successVals:
                raise RuntimeError("Could not find a valid device.")
            break

    if not devicePort:
        raise RuntimeError("Could not find a valid device.")

    return devicePort


# ============================================
#                 _timed_open
# ============================================
def _timed_open(clib, port, baudRate, logLevel):
    return clib.open(port.encode("utf-8"), baudRate, logLevel)
