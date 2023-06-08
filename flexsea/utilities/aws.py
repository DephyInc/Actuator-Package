import hashlib
from pathlib import Path
from typing import List

from cloudpathlib import CloudPath
from cloudpathlib import S3Client


# ============================================
#                 s3_download
# ============================================
def s3_download(obj: str, bucket: str, dest: str, profile: str | None = None) -> None:
    """
    Downloads `obj` from `bucket` to `dest` with the AWS
    credentials profile `profile`.
    """
    noSign = not profile
    client = S3Client(
        no_sign_request=noSign,
        profile_name=profile,
        extra_args={"ChecksumMode": "ENABLED"},
    )
    cloudpath = client.CloudPath(f"s3://{bucket}/{obj}")

    if not cloudpath.exists():
        raise FileNotFoundError(f"Error: could not find: {bucket}/{obj} for download.")

    cloudpath.download_to(dest)
    if cloudpath.is_file():
        _validate_download(cloudpath, dest)
    else:
        # Might be slow depending on number of files and file size
        for path in cloudpath.rglob("**/*"):
            if path.is_file():
                _validate_download(path, path.fspath)

    client.clear_cache()


# ============================================
#             _validate_download
# ============================================
def _validate_download(cloudpath: CloudPath, localFile: str) -> None:
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
    """
    try:
        assert Path(localFile).exists()
    except AssertionError as err:
        raise RuntimeError(f"Failed to download `{localFile}`") from err

    etag = cloudpath.etag.strip('"')

    try:
        nChunks = int(etag.split("-")[1])
    except IndexError:
        nChunks = 1

    if nChunks == 1:
        with open(localFile, "rb") as fd:
            data = fd.read()
        localHash = hashlib.md5(data).hexdigest()

    elif nChunks > 1:
        chunkHashes = []
        with open(localFile, "rb") as fd:
            for chunk in range(1, nChunks + 1):
                objData = cloudpath.client.client.head_object(
                    Bucket=cloudpath.bucket, Key=cloudpath.key, PartNumber=chunk
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

    try:
        assert localHash == etag
    except AssertionError as err:
        raise RuntimeError(
            f"Error: {localFile} download failed. Hashes don't match."
        ) from err


# ============================================
#                s3_search
# ============================================
def s3_search(bucket: str, pattern: str, profile: str | None = None) -> List[CloudPath]:
    noSign = not profile
    client = S3Client(no_sign_request=noSign, profile_name=profile)
    cloudpath = client.CloudPath(f"s3://{bucket}")
    objs = []
    for obj in cloudpath.rglob(pattern):
        objs.append(obj)
    client.clear_cache()
    return objs
