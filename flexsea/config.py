from pathlib import Path


# ============================================
#              Path Configuration
# ============================================
cacheDir = Path.joinpath(Path.home(), ".dephy", "flexsea")
libsDir = cacheDir.joinpath("libs")


# ============================================
#              S3 Configuration
# ============================================
libsBucket = "dephy-public-binaries"
