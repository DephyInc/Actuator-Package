"""
utils.py

Contains utility functions used by the demos.
"""
import os
from os.path import abspath
from os.path import dirname
from os.path import expanduser
from os.path import expandvars
from os.path import isfile
from os.path import join
import shutil
import stat as st

from cleo.config import ApplicationConfig as BaseApplicationConfig
from clikit.api.formatter import Style
from flexsea import flexsea as flex
import yaml


# ============================================
#                    setup
# ============================================
def setup(cls, schema, param_file, demo_name):
	"""
	Contains the boilerplate code for setting up a demo.

	Parameters
	----------
	cls : cleo.Command
		The instance of the demo command to set up.

	schema : dict
		Names and types of the parameters required by the demo. Used to
		validate the data read from the parameter file.

	param_file : str
		Name (and path) of the parameter file to read.

	demo_name : str
		Name of the demo being run (e.g., read_only).
	"""
	demo_params = {}
	# Read parameter file, if given
	if param_file:
			demo_params = read_param_file(param_file, demo_name)
	# Check for command-line option overrides
	# pylint: disable=protected-access
	demo_params = get_cli_overrides(cls._args.options(), schema, demo_params)
	# Validate and assign
	demo_params = validate(schema, demo_params)
	assign_params(cls, demo_params)
	setattr(cls, "fxs", flex.FlexSEA())


# ============================================
#              read_param_file
# ============================================
def read_param_file(param_file, demo_name):
	"""
	Reads the parameters for the desired demo from the parameter file.
	If the given parameter file is read-only, we make a copy of it and
	work with the copy.

	Parameters
	----------
	param_file : str
		Name of the parameter file to read.

	demo_name : str
		The desired demo to be run.

	Returns
	-------
	dict
		Demo-specific parameters read from the given file.
	"""
	if is_lock_file(param_file):
		param_file = copy_param_file(param_file)
	all_params = read_yaml(param_file)
	return get_demo_params(all_params, demo_name)


# ============================================
#              get_cli_overrides
# ============================================
def get_cli_overrides(opts, schema, demo_params):
	"""
	Checks to see if any of the demo's parameters from the parameter
	file have been overridden on the command-line.

	Parameters
	----------
	opts : dict
		Contains all available command-line options for the given demo.
		If the option isn't set, it will be None if the option needs a
		value and False if it's a flag.

	schema : dict
		Contains the names and data types for the parameters required
		by the demo.

	demo_params : dict
		Contains the parameters read in from the parameter file. If
		one wasn't passed, then it's an empty dictionary.

	Returns
	-------
	dict
		`demo_params` but updated to reflect the command-line values.
	"""
	for key, data_type in schema.items():
		# Cleo requires that options only contain letters, numbers, and hyphens,
		# so in order to match the underscore version used in the code we need
		# to replace
		cli_key = key.replace("_", "-")
		if opts[cli_key] is not None:
			# Ports and gains are two special cases
			# Since ports and gains are multi-valued option, their default
			# value is [] when nothing is passed to it, not None
			if key == "ports":
				if len(opts[cli_key]) > 0:
					demo_params[key] = [p for p in opts[cli_key][0].split(",")]
			elif key == "gains":
				if len(opts[cli_key]) > 0:
					names = ["KP", "KI", "KD", "K", "B", "FF"]
					vals = [int(g) for g in opts[cli_key][0].split(",")]
					demo_params[key] = dict(zip(names, vals))
			else:
				demo_params[key] = cast(opts[cli_key], data_type)
	return demo_params


# ============================================
#                   cast
# ============================================
def cast(value, data_type):
	"""
	Cleo reads all command-line options as strings, but the demos
	require some of them to be converted to other types, as specified
	in schema for that demo. This function handles that conversion.

	Note that boolean options, i.e. those passed without a value, are
	already stored as a bool by cleo. As such, for those values whose
	data type is str or bool, nothing needs to be done, as they are
	already the correct type.

	Parameters
	----------
	value : str
		The value of the parameter read from the command-line.

	data_type : Union[int, float, str, bool]
		The data type of `value` as specified by the demo's schema.

	Returns
	-------
	Union[int, float, str, bool]
		`value` as `data_type`.
	"""
	if data_type == int:
		value = int(value)
	elif data_type == float:
		value = float(value)
	return value


# ============================================
#               get_demo_params
# ============================================
def get_demo_params(all_params, demo_name):
	"""
	The parameter file contains parameters for each demo. This extracts
	only those parameters corresponding to the demo actually being run.

	Parameters
	----------
	all_params : dict
		The parameter/value pairs read in.

	demo_name : str
		The name of the demo being run (e.g., read_only).

	Returns
	-------
	dict
		A dictionary containing only those parameters pertaining to the
		demo being run.
	"""
	demo_params = all_params.pop(demo_name)
	demo_params.update(all_params.pop("general"))
	return demo_params


# ============================================
#                  validate
# ============================================
def validate(schema, data):
	"""
	Makes sure that `data` has the keys contained in `schema` and that
	the values in `data` are of the type specified in `schema`.

	Parameters
	----------
	schema : dict
		Keys are the names of the required parameters and the values
		are the types required for the corresponding parameter.

	data : dict
		The parameter/value pairs read in.

	Returns
	-------
	data : dict
		The validated data.
	"""
	for required_param, required_param_type in schema.items():
		try:
			assert required_param in data.keys()
		except AssertionError as err:
			raise AssertionError(f"'{required_param}' not found.") from err
		try:
			assert isinstance(data[required_param], required_param_type)
		except AssertionError as err:
			msg = f"'{required_param_type}' isn't the right type for '{required_param}'."
			raise AssertionError(msg) from err
	return data


# ============================================
#               assign_params
# ============================================
def assign_params(cls, params):
	"""
	Sets the values of the parameters in `params` as attributes of the
	class `cls`.

	Parameters
	----------
	cls : cle.Command
		The Command class for which we are setting attributes.

	params : dict
		Contains the attribute names and values to use as attributes.
	"""
	for key, value in params.items():
		setattr(cls, key, value)


# ============================================
#                  read_yaml
# ============================================
def read_yaml(yaml_file):
	"""
	Contains the boilerplate code for reading a yaml file.

	Parameters
	----------
	yaml_file : str
		The name (including path) of the yaml file to read.

	Returns
	-------
	dict
		A dictionary containing the data read from the file.
	"""
	yaml_file = sanitize_path(yaml_file)
	with open(yaml_file, "r", encoding="utf-8") as in_file:
		data = yaml.safe_load(in_file)
	return data


# ============================================
#                sanitize_path
# ============================================
def sanitize_path(path):
	"""
	Expands out environment variables, handles links, and makes sure
	that the file exists.

	Parameters
	----------
	path : str
		The path to clean.

	Raises
	------
	FileNotFoundError
		If the given path cannot be found.

	Returns
	-------
	str
		The expanded path.
	"""
	path = expandvars(path)
	path = expanduser(path)
	path = abspath(path)
	if not isfile(path):
		raise FileNotFoundError(f"Could not file parameter file: '{path}'")
	return path


# ============================================
#                is_lock_file
# ============================================
def is_lock_file(param_file):
	"""
	Checks to see if the given file has write permissions or has a 'lock'
	extension.

	Parameters
	----------
	param_file : str
		Name of the file to check.

	Returns
	-------
	bool
		Whether or not the file is a lock file.
	"""
	if param_file.endswith(".lock"):
		return True
	info = os.stat(param_file)
	return not bool(info.st_mode & st.S_IWUSR)


# ============================================
#                copy_param_file
# ============================================
def copy_param_file(param_file):
	"""
	In the case that we're given a locked file as the parameter file,
	we make a copy of the file, give that copy read and write
	permissions, and then return the name of the copied file to be
	read.

	Parameters
	----------
	param_file : str
		The name (and path) of the locked parameter file.

	Returns
	-------
	copied_file : str
		A file named 'params_copy.yaml' that lives alongside
		`param_file`, has the same contents, but has read and write
		permissions.
	"""
	path = dirname(abspath(param_file))
	copied_file = join(path, "params_copy.yaml")
	shutil.copy(param_file, copied_file)
	mode = st.S_IRUSR | st.S_IWUSR | st.S_IRGRP | st.S_IWGRP | st.S_IROTH | st.S_IWOTH
	os.chmod(copied_file, mode)
	return copied_file


# ============================================
#              ApplicationConfig
# ============================================
class ApplicationConfig(BaseApplicationConfig):
	"""
	Handles configuration of the CLI.
	"""

	def configure(self):
		super().configure()
		self.add_style(Style("info").fg("cyan"))
		self.add_style(Style("error").fg("red").bold())
		self.add_style(Style("warning").fg("yellow").bold())
		self.add_style(Style("success").fg("green"))
