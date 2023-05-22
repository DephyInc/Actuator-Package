import hashlib
from pathlib import Path
from typing import List

import boto3
from botocore import UNSIGNED
from botocore.client import BaseClient, Config
from botocore.exceptions import ClientError


# ============================================
#                 s3_download
# ============================================
def s3_download(obj: str, bucket: str, dest: str, profile: str | None = None) -> None:
    """
    Downloads `obj` from `bucket` to `dest` with the AWS
    credentials profile `profile`.
    """
    # https://stackoverflow.com/a/34866092
    if profile is None:
        client = boto3.client(
            "s3", config=Config(signature_version=UNSIGNED), region_name="us-east-1"
        )
    else:
        session = boto3.Session(profile_name=profile)
        client = session.client("s3")

    try:
        client.download_file(bucket, obj, dest)
    except ClientError:
        # If the download fails, one possible reason is because we weren't given a
        # valid object path, but, instead, just a base name, e.g., myfirmware.dfu
        # instead of firmwareBucket/major.minor.patch/device/hw/myfirmware.dfu
        # In this case we want to search the given bucket for the file
        obj = s3_find_object(obj, bucket, client)
        client.download_file(bucket, obj, dest)
    _validate_download(client, bucket, obj, dest)


# ============================================
#              s3_find_object
# ============================================
def s3_find_object(fileName: str, bucket: str, client: str) -> str:
    """
    Searches the given bucket for the given file. Returns the full object
    path if there's only one match. If there aren't any matches or there's
    more than one, we fail.
    """
    # https://tinyurl.com/4scnuk6c
    paginator = client.get_paginator("list_objects_v2")
    pageIterator = paginator.paginate(Bucket=bucket)
    objects = pageIterator.search(f"Contents[?contains(Key, `{fileName}`)][]")
    # There should only be one match
    # Objects is a generator, so we have to convert it to a list to check length
    items = []
    for item in objects:
        items.append(item["Key"])
    if len(items) == 0:
        raise FileNotFoundError(f"Could not find: {fileName} in {bucket}")
    if len(items) > 1:
        raise FileNotFoundError(f"Found multiple options for: {fileName} in {bucket}")
    return items[0]


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

    Raises
    -------
    FileNotFoundError
        If the downloaded file is not present in the desired destinationself.

    AssertionError
        If the hash of the remote object does not match the hash of the local
        file.
    """
    try:
        assert Path(dest).exists()
    except AssertionError as err:
        raise FileNotFoundError from err

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
#                get_s3_objects
# ============================================
def get_s3_objects(bucket: str, client: BaseClient, prefix: str = "") -> List:
    """
    Recursively loops over all directories in a bucket and returns a
    list of files.

    Parameters
    ----------
    bucket : str
        The name of the bucket we're getting files from.

    client : botocore.client.BaseClient
        The object providing an interface to S3.

    prefix : str
        The directory we're looping over. If `""`, then we get the
        top-level directories.

    Returns
    -------
    List[str]
        A list of all the objects in the bucket.
    """
    objectList = []
    objects = client.list_objects_v2(Bucket=bucket, Delimiter="/", Prefix=prefix)

    if "CommonPrefixes" in objects:
        for pre in objects["CommonPrefixes"]:
            objectList += get_s3_objects(bucket, client, pre["Prefix"])

    if "Contents" in objects:
        return objectList + [obj["Key"] for obj in objects["Contents"][1:]]
    return objectList
