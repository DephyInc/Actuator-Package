"""
FlexSEA package setup info
"""
import os
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
	LONG_DESCRIPTION = fh.read()

lib_files_location = os.path.join(
	os.path.dirname(os.path.realpath(__file__)), "..", "..", "libs"
)
inc_files_location = os.path.join(
	os.path.dirname(os.path.realpath(__file__)), "..", "..", "inc"
)


def package_files(directory):
	"""Add files to package"""
	paths = []
	for (path, _directories, filenames) in os.walk(directory):
		for filename in filenames:
			paths.append(os.path.join("..", path, filename))
	return paths


if not os.path.exists(lib_files_location):
	raise FileNotFoundError("Required libraries for the build was not found!")

if not os.path.exists(inc_files_location):
	raise FileNotFoundError("Required source for the build was not found!")

libs = package_files(lib_files_location)
inc = package_files(inc_files_location)

setuptools.setup(
	name="flexsea",  # Replace casmat with other username if needed
	version="7.0.0",
	author="Dephy Inc.",
	author_email="admin@dephy.com",
	description="Dephy's Actuator Package API library",
	long_description=LONG_DESCRIPTION,
	long_description_content_type="text/markdown",
	url="https://github.com/DephyInc/Actuator-Package/",
	packages=setuptools.find_packages(),
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
	python_requires=">= 3.8.*",
	include_package_data=True,
	package_data={"libs": libs, "inc": inc},
)
