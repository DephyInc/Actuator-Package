"""
Entry point for the flexsea demos CLI.
"""
from .app import FlexseaDemoApplication


# ============================================
#                    main
# ============================================
def main():
	"""
	Creates and runs an instance of the flexsea demo CLI.
	"""
	FlexseaDemoApplication().run()
