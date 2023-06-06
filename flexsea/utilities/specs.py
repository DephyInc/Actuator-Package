from cloudpathlib import CloudPath
import yaml
from semantic_version import Version

import flexsea.utilities.constants as fxc


# ============================================
#               get_device_spec
# ============================================
def get_device_spec(deviceName: str, firmwareVersion: Version) -> dict:
    deviceSpecFile = fxc.legacyDeviceSpecsPath.joinpath(
        str(firmwareVersion), f"{deviceName}.yaml"
    )

    if not deviceSpecFile.exists():
        deviceSpecFile.parent.mkdir(parents=True, exist_ok=True)
        objName = f"s3://{fxc.dephyPublicFilesBucket}/{fxc.legacyDeviceSpecsDir}/"
        objName += f"{firmwareVersion}/{deviceSpecFile.name}"
        obj = CloudPath(objName)

        # We do this because cloudpathlib doesn't raise an exception when downloading
        # a file that doesn't exist
        if not obj.is_file():
            raise FileNotFoundError("Error: could not find `{deviceSpecFile.name}`.")

        obj.download_to(deviceSpecFile)

    with open(deviceSpecFile, "r", encoding="utf-8") as fd:
        deviceSpec = yaml.safe_load(fd)

    return deviceSpec
