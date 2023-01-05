import os

from flexsea.utilities import get_os


# ============================================
#                clear_terminal
# ============================================
def clear_terminal():
    """
    Clears the terminal - use before printing new values
    """
    os.system("cls" if "windows" in get_os() else "clear")
