# ============================================
#      validate_given_firmware_version
# ============================================
def validate_given_firmware_version(firmwareVersion: str, interactive: bool) -> Version:
    availableVersions = get_available_firmware_versions()

    # First we check if the user gave us a complete version string,
    # e.g., 7.2.0
    try:
        firmwareVersion = Version(firmwareVersion)
    except ValueError:
        # Check if the user gave us a partial version string, e.g., 7
        try:
            firmwareVersion = Version.coerce(firmwareVersion)
        except ValueError:
            msg = f"Error: could not cast given version {firmwareVersion} to a valid "
            msg += "semantic version string. Please use the form X.Y.Z, where X, Y, "
            msg += "and Z are integers. For valid versions, please see: "
            msg += "flexsea.utilities.firmware.get_available_firmware_versions()"
            print(msg)
            sys.exit(1)

        # If the user did give us a partial version string, we now want
        # to find the most recent version that shares a major version
        # with what the user gave us. E.g., if the user gave us 7 and
        # the list of available versions contains 7.2.3 and 7.4.5, we
        # want to use 7.4.5
        latestVer = get_closest_version(firmwareVersion, availableVersions)
        if firmwareVersion != latestVer:
            msg = f"Warning: received version {firmwareVersion}, but found: "
            msg += f"{latestVer}, which is newer."
            print(msg)
            if interactive:
                userInput = input(f"Use {latestVer}? [y/n]")
                if userInput.lower() == "y":
                    firmwareVersion = latestVer
                else:
                    print("Aborting: no valid version selected.")
                    sys.exit(1)
            else:
                firmwareVersion = latestVer
    # If the user did give us a full version string, we make sure that
    # it's in the list of known versions
    else:
        try:
            assert str(firmwareVersion) in availableVersions
        except AssertionError:
            msg = f"Error: no library found for version: {firmwareVersion}. Use "
            msg += "flexsea.utilities.firmware.get_available_firmware_versions() "
            msg += "to see the available versions."
            sys.exit(1)

    return firmwareVersion


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
            with open(fxc.firmwareVersionCacheFile, "r") as fd:
                    data = yaml.safe_load(fd)
        except FileNotFoundError:
            msg = "Error: no firmware version cache file found. "
            msg += "Try connecting to the internet and running this function again."
            print(msg)
            sys.exit(1)
        libs = data["versions"]
        days = (pendulum.today() - pendulum.parse(data["date"])).days
        print(f"Warning: using firmware version information from: {days} ago.")
        print("To update, connect to the internet and re-run this function.")
    else:
        libs = set()
        for obj in objs:
            lib = obj.split("/")[1]
            libs.add(lib)
        libs = sorted(list(libs))

        with open(fxc.firmwareVersionCacheFile, "w") as fd:
            yaml.safe_dump({"date":str(pendulum.today()), "versions":libs}, fd)
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
