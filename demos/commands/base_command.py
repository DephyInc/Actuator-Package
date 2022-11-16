# ============================================
#              BaseDemoCommand
# ============================================
class BaseDemoCommand(Command):
    # -----
    # constructor
    # -----
    def __init__(self, demoName: str, schema: Dict, options: List) -> None:
        super().__init__()

        self.devices = []
        self.baudRate = 0
        self.streamingFrequency = 0
        self.runTime = 0
        self.gains = {}
        self.cLibVersion = ""

        # Parse param file and/or cl options
        # Create device(s) instance(s). Use auto-search
