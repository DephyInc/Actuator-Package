"""
FlexSEA package setup info
"""
import os
from shutil import copytree, rmtree
import setuptools

PKG_NAME = "flexsea"

with open("README.md", "r", encoding="utf-8") as fh:
	LONG_DESCRIPTION = fh.read()

lib_files_location = os.path.join("..", "..", "libs")
inc_files_location = os.path.join("..", "..", "inc")
lib_files_dest = os.path.join("flexsea", "libs")
inc_files_dest = os.path.join("flexsea", "inc")

if not os.path.exists(lib_files_location):
	raise FileNotFoundError("Required libraries for the build was not found!")

if not os.path.exists(inc_files_location):
	raise FileNotFoundError("Required source for the build was not found!")

# Clean old library and include files
try:
	rmtree(lib_files_dest)
	rmtree(inc_files_dest)
except FileNotFoundError:
	pass

# Copy over new libraries
copytree(lib_files_location, lib_files_dest)
copytree(inc_files_location, inc_files_dest)


def get_files(location):
	"""Find lib file locations"""
	paths = []
	for (path, _directories, filenames) in os.walk(location):
		for filename in filenames:
			# Constraint of new setuptools which require forward slash to resolve path separator.
			# No matter what OS
			paths.append(os.path.join(path, filename).replace("\\", "/"))
	return paths


print(
	"Libs locaiton: {0}\nInc location: {1}".format(lib_files_location, inc_files_location)
)

lib_files = get_files(lib_files_dest)
inc_files = get_files(inc_files_dest)
print("Lib files:\n{}".format(lib_files))
print("inc files:\n{}".format(inc_files))

setuptools.setup(
	name="flexsea",
	version="7.2.3",
	author="Dephy Inc.",
	author_email="admin@dephy.com",
	description="Dephy's Actuator Package API library",
	long_description=LONG_DESCRIPTION,
	long_description_content_type="text/markdown",
	url="https://github.com/DephyInc/Actuator-Package/",
	packages=setuptools.find_packages(),
	package_dir={"flexsea": "flexsea"},
	install_requires=[
		"scipy==1.*",
		"tornado==6.*",
		"matplotlib==3.*",
		"numpy==1.*",
		"pillow==8.*",
		"PyYAML==5.*",
	],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
		"Operating System :: POSIX :: Linux",
		"Operating System :: Microsoft :: Windows :: Windows 10",
		"Development Status :: 5 - Production/Stable",
	],
	python_requires=">= 3.7.*",
	include_package_data=True,
	data_files=[("libs", lib_files), ("inc", inc_files)],
)
