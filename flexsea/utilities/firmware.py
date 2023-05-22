import ctypes as c
from typing import List

import boto3
from semantic_version import SimpleSpec, Version

import flexsea.utilities.constants as fxc
from flexsea.utilities.aws import get_s3_objects


# ============================================
#       get_available_firmware_versions
# ============================================
def get_available_firmware_versions() -> List[str]:
    session = boto3.Session()
    client = session.client("s3")

    objs = get_s3_objects(fxc.dephyPublicFilesBucket, client, prefix=fxc.libsDir)

    client.close()

    libs = set()

    for obj in objs:
        lib = obj.split("/")[1]
        libs.add(lib)

    return sorted(list(libs))


# ============================================
#      validate_given_firmware_version
# ============================================
def validate_given_firmware_version(firmwareVersion: str, interactive: bool) -> Version:
    try:
        fwVer = Version(firmwareVersion)
    except ValueError as err:
        # If we're not given a valid semantic version string, we'll
        # find the latest available version with the same major version
        # as that of `firmwareVersion`
        fwVer = Version.coerce(firmwareVersion)
        latestVer = get_closest_version(fwVer)
        if fwVer != latestVer:
            msg = f"WARNING: Received version: {firmwareVersion}, but found: "
            msg += f"{latestVer}, which is newer."
            print(msg)
            if interactive:
                userInput = input(f"Use {latestVer}? [y/n]")
                if userInput.lower() == "y":
                    fwVer = latestVer
                else:
                    raise RuntimeError("Aborting: no valid version selected.") from err
            else:
                fwVer = latestVer
    else:
        try:
            assert str(fwVer) in get_available_firmware_versions()
        except AssertionError as err:
            msg = f"Error: no library found for version: {fwVer}. Use "
            msg += "flexsea.utilities.firmware.get_available_firmware_versions() "
            msg += "to see the available versions."
            raise ValueError(msg) from err

    return fwVer


# ============================================
#             get_closest_version
# ============================================
def get_closest_version(version: Version) -> Version:
    availableVersions = get_available_firmware_versions()

    # https://tinyurl.com/3e4t6svb
    versionSpec = SimpleSpec(f"~={version.major}")
    closestVersion = versionSpec.select([Version(v) for v in availableVersions])

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
