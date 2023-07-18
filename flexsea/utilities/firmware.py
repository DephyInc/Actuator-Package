import ctypes as c
import sys
from typing import List

import boto3
from botocore import UNSIGNED
from botocore.client import Config
from botocore.exceptions import EndpointConnectionError
import pendulum
from semantic_version import SimpleSpec
from semantic_version import Version
import yaml

from flexsea.utilities.aws import get_s3_objects
import flexsea.utilities.constants as fxc


# ============================================
#      validate_given_firmware_version
# ============================================
def validate_given_firmware_version(firmwareVersion: str, interactive: bool) -> Version:
    availableVersions = get_available_firmware_versions()

    if firmwareVersion in availableVersions:
        return Version(firmwareVersion)

    try:
        firmwareVersion = Version.coerce(firmwareVersion)
    except ValueError as err:
        msg = f"Error: could not cast given version {firmwareVersion} to a valid "
        msg += "semantic version string. Please use the form X.Y.Z, where X, Y, "
        msg += "and Z are integers. For valid versions, please see: "
        msg += "flexsea.utilities.firmware.get_available_firmware_versions()"
        raise ValueError(msg) from err

    # Check for latest available version with the same major version as
    # the given version
    latestVer = get_closest_version(firmwareVersion, availableVersions)
    msg = f"Warning: received version {firmwareVersion}, but found: "
    msg += f"{latestVer}, which is newer."
    print(msg)
    if interactive:
        userInput = input(f"Use {latestVer}? [y/n]")
        if userInput.lower() != "y":
            print("Aborting: no valid version selected.")
            sys.exit(1)
    return latestVer


# ============================================
#       get_available_firmware_versions
# ============================================
def get_available_firmware_versions() -> List[str]:
    """
    To facilitiate offline use and firmware version validation, we
    cache a list of the currently available versions each time this
    function is run while online. If the user is not online, we load
    the available versions from the previously cached file and warn
    the user about how long it has been since their information was
    updated. If the file doesn't exist and we're not online, then
    the version information cannot be obtained, so we exit.
    """
    client = boto3.client(
        "s3", config=Config(signature_version=UNSIGNED), region_name="us-east-1"
    )

    try:
        objs = get_s3_objects(fxc.dephyPublicFilesBucket, client, prefix=fxc.libsDir)
    except EndpointConnectionError:
        print("Warning: unable to access S3 to obtain updated available versions.")
        try:
            with open(fxc.firmwareVersionCacheFile, "r", encoding="utf-8") as fd:
                data = yaml.safe_load(fd)
        except FileNotFoundError as err:
            msg = "Error: no firmware version cache file found. "
            msg += "Try connecting to the internet and running this function again."
            print(msg)
            raise err
        libs = data["versions"]
        days = (pendulum.today() - pendulum.parse(data["date"])).days
        if days > 7:
            print(f"Warning: using firmware version information from: {days} days ago.")
            print("To update, connect to the internet and re-run this function.")
    else:
        libs = set()
        for obj in objs:
            lib = obj.split("/")[1]
            libs.add(lib)
        libs = sorted(list(libs))

        with open(fxc.firmwareVersionCacheFile, "w", encoding="utf-8") as fd:
            yaml.safe_dump({"date": str(pendulum.today()), "versions": libs}, fd)
    finally:
        client.close()

    return libs


# ============================================
#             get_closest_version
# ============================================
def get_closest_version(version: Version, versionList: List[str]) -> Version:
    # https://tinyurl.com/3e4t6svb
    versionSpec = SimpleSpec(f"~={version.major}")
    closestVersion = versionSpec.select([Version(v) for v in versionList])

    if closestVersion is None:
        raise RuntimeError(f"Could not find version: {version}")

    return closestVersion


# ============================================
#                  Firmware
# ============================================
class Firmware(c.Structure):
    """
    Holds the integer values representing the firmware versions of
    each microcontroller as returned from the C library. These need to
    be decoded before they make sense.
    """

    _fields_ = [
        ("mn", c.c_uint32),
        ("ex", c.c_uint32),
        ("re", c.c_uint32),
        ("habs", c.c_uint32),
    ]


# ============================================
#              decode_firmware
# ============================================
def decode_firmware(val: int) -> str:
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
