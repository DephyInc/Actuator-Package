from botocore.exceptions import EndpointConnectionError
import yaml
from semantic_version import Version

import flexsea.utilities.constants as fxc
from flexsea.utilities.aws import s3_download


# ============================================
#               get_device_spec
# ============================================
def get_device_spec(deviceName: str, firmwareVersion: Version) -> dict:
    deviceSpecFile = fxc.legacyDeviceSpecsPath.joinpath(
        str(firmwareVersion), f"{deviceName}.yaml"
    )

    if not deviceSpecFile.exists():
        deviceSpecFile.parent.mkdir(parents=True, exist_ok=True)
        deviceSpecObj = (
            f"{fxc.legacyDeviceSpecsDir}/{firmwareVersion}/{deviceSpecFile.name}"
        )
        try:
            s3_download(
                deviceSpecObj, fxc.dephyPublicFilesBucket, str(deviceSpecFile), None
            )
        except EndpointConnectionError as err:
            msg = "Error: could not connect to the internet to download the "
            msg += "necessary device spec file. Please connect to the internet and "
            msg += "try again."
            print(msg)
            raise err

    with open(deviceSpecFile, "r", encoding="utf-8") as fd:
        deviceSpec = yaml.safe_load(fd)

    return deviceSpec
