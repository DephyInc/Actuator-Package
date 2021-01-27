"""
FlexSEA package setup info
"""
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
	LONG_DESCRIPTION = fh.read()

setuptools.setup(
	name="flexsea",  # Replace with your own username
	version="4.3.0",
	author="Dephy Inc.",
	author_email="admin@dephy.com",
	description="Dephy's Actuator Package API library",
	long_description=LONG_DESCRIPTION,
	long_description_content_type="text/markdown",
	url="https://github.com/DephyInc/Actuator-Package/",
	packages=setuptools.find_packages(),
	install_requires=[
		"scipy==1.5.*",
		"tornado==6.0.*",
		"matplotlib==3.3.*",
		"numpy==1.19.*",
		"pillow==8.1.*",
	],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
		"Operating System :: POSIX :: Linux",
		"Operating System :: Microsoft :: Windows :: Windows 10",
		"Development Status :: 5 - Production/Stable",
	],
	python_requires="== 3.7.*",
	package_data={"libs": ["../../libs"], "inc": ["../../inc"], "": ["README.md"],},
)
