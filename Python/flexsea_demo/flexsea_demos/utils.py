import os

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
	all_params = read_yaml(param_file)
	demo_params = get_demo_params(all_params, demo_name)
	demo_params = validate(schema, demo_params)
	assign_params(cls, demo_params)
	setattr(cls, "fxs", flex.FlexSEA())


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
	path = os.path.expandvars(path)
	path = os.path.expanduser(path)
	path = os.path.abspath(path)
	if not os.path.isfile(path):
		raise FileNotFoundError(f"Could not file parameter file: '{path}'")
	return path


# ============================================
#              ApplicationConfig
# ============================================
class ApplicationConfig(BaseApplicationConfig):
	def configure(self):
		super().configure()
		self.add_style(Style("info").fg("cyan"))
		self.add_style(Style("error").fg("red").bold())
		self.add_style(Style("warning").fg("yellow").bold())
		self.add_style(Style("success").fg("green"))
