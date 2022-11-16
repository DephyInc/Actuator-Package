from .application import FlexseaDemoApplication


# ============================================
#                     main
# ============================================
def main() -> None:
    """
    Entry point.

    Creates an instance of the command-line interface (CLI) object and
    runs it.
    """
    FlexseaDemoApplication().run()
