"""
device.py

Contains the device class.
"""
from time import sleep

from flexsea import fxEnums as fxe
from flexsea import fxUtils as fxu


# ============================================
#                   Device
# ============================================
class Device:
	"""
	Contains and manages the actpack/exoboot information and state.
	"""

	# pylint: disable=too-many-instance-attributes

	# -----
	# constructor
	# -----
	def __init__(self, fxs, port, baud_rate, **kwargs):
		# NOTE: Can fxs be passed around like this?
		self.fxs = fxs
		self.port = port
		self.baud_rate = baud_rate
		for key, value in kwargs.items():
			setattr(self, key, value)

		self.dev_id = self.fxs.open(self.port, self.baud_rate, 0)
		self.fxs.start_streaming(self.dev_id, freq=100, log_en=True)
		# NOTE: This sleep is so long because there's an issue that
		# occurs when trying to open multiple devices in rapid
		# succession that causes flexsea to crash
		sleep(1)
		self.app_type = self.fxs.get_app_type(self.dev_id)

		if self.app_type.value == fxe.FX_INVALID_APP.value:
			raise KeyError(f"Invalid app type: '{self.app_type.value}'")

		try:
			app_name = fxe.APP_NAMES[self.app_type.value]
		except KeyError as err:
			raise RuntimeError(f"Unsupported application type: {self.app_type.value}") from err

		print(f"Your device is an '{app_name}'", flush=True)

		self.initial_pos = self.get_pos()
		self.controller_type = None
		self.controller = None

	# -----
	# motor
	# -----
	def motor(self, component, value):
		"""
		Sends a command to the device motor.

		Parameters
		----------
		component : int
			A flexsea enumeration value indicating voltage, current, etc.

		value : float
			The value to send.
		"""
		self.fxs.send_motor_command(self.dev_id, component, value)

	# -----
	# read
	# -----
	def read(self):
		"""
		Reads the current state of the device.
		"""
		return self.fxs.read_device(self.dev_id)

	# -----
	# print
	# -----
	def print(self, data=None):
		"""
		Reads the data from the device and then prints it to the screen.
		"""
		if not data:
			data = self.read()
		fxu.print_device(data, self.app_type)

	# -----
	# set_gains
	# -----
	def set_gains(self, gains):
		"""
		Sets the gains on the device. Gains are, in order:
		kp, ki, kd, K, B & ff
		"""
		# TODO(CA): Investigate this problem and remove the hack below
		# Set gains several times since they might not get set when only set once.
		for _ in range(5):
			self.fxs.set_gains(
				self.dev_id,
				gains["KP"],
				gains["KI"],
				gains["KD"],
				gains["K"],
				gains["B"],
				gains["FF"],
			)

	# -----
	# get_pos
	# -----
	def get_pos(self):
		"""
		Returns the current position of the device.
		"""
		return self.read().mot_ang

	# -----
	# activate_bootloader
	# -----
	def activate_bootloader(self, target):
		"""
		Activates the device's bootloader.
		"""
		self.fxs.activate_bootloader(self.dev_id, target)

	# -----
	# is_bootloader_activated
	# -----
	def is_bootloader_activated(self):
		"""
		Checks to see if the device's bootloader is active.
		"""
		return self.fxs.is_bootloader_activated(self.dev_id)

	# -----
	# request_firmware_version
	# -----
	def request_firmware_version(self):
		"""
		Gets the device's firmware versions.
		"""
		return self.fxs.request_firmware_version(self.dev_id)

	# -----
	# get_last_received_firmware_version
	# -----
	def get_last_received_firmware_version(self):
		"""
		Gets the last read firmware versions.
		"""
		return self.fxs.get_last_received_firmware_version(self.dev_id)

	# -----
	# set_controller
	# -----
	def set_controller(self, controller_type):
		"""
		Sets the device's controller.
		"""
		self.controller_type = controller_type
		if self.controller_type == fxe.HSS_CURRENT:
			self.controller = fxe.FX_CURRENT
		elif self.controller_type == fxe.HSS_POSITION:
			self.controller = fxe.FX_POSITION

	# -----
	# close
	# -----
	def close(self):
		"""
		Shuts down the device.
		"""
		self.fxs.close(self.dev_id)
