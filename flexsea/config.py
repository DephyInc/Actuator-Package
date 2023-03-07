from pathlib import Path

# ============================================
#             Path Configuration
# ============================================
dephyDir = Path.home().joinpath(".dephy")
libsDir = dephyDir.joinpath("libs")
windowsLib = "libfx_plan_stack.dll"
linuxLib = "libfx_plan_stack.so"


# ============================================
#              S3 Configuration
# ============================================
libsBucket = "dephy-public-binaries"


# ============================================
#           Version Configuration
# ============================================
LTS = "7.2.0"
legacyCutoff = "10.0.0"


# ============================================
#                 Constants
# ============================================
baudRate = 230400
