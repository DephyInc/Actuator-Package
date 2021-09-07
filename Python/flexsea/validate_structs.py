#!/usr/bin/env python3
"""Validate C structs"""

from signal import signal, SIGINT
import os
import sys
import ast
import pyclibrary

C_STRUCTS_DIR = os.path.join(os.getcwd(), "flexsea", "inc")
PYTHON_DIR = os.path.join(os.getcwd(), "flexsea", "dev_spec")
IGNORE_FILES = ["__init__.py", "__pycache__", "AllDevices.py"]
COMPARE_FILE = os.path.join(os.getcwd(), "py-c-files.config")


def sig_handler(_frame, _signal_received):
	"""Handle keyboard interrupt"""
	return sys.exit("\nCTRL-C or SIGINT detected\nExiting ...")


def find_files(file_path, ignore_list, strip_characters):
	"""
	Filter only files that we are concerned with. Endswith: *State.py
	"""
	files_found = [
		file
		for file in os.listdir(file_path)
		if file not in ignore_list
		if file.endswith(strip_characters)
	]
	# strip filenames
	files_found = [file[: -len(strip_characters)] for file in files_found]
	return files_found


def extract_py_fields(ast_fields):
	"""
	extract fields
	"""
	fields = []
	for each_tup in ast_fields:
		fields.append(each_tup.elts[0].s)
	fields = [field for field in fields if not field.endswith("SystemTime")]
	return fields


def extract_py_node(class_node):
	"""
	extract nodes
	"""
	all_nodes = list(ast.iter_child_nodes(class_node))
	fields_extracted = []
	if len(all_nodes) != 2:
		print("ERR: Bad parsing in py files! Something has changed. Contact the developers!")
		return fields_extracted
	if not (isinstance(all_nodes[0], ast.Name) and all_nodes[0].id == "_fields_"):
		print("ERR - Bad parsing in py files! Something has changed. Contact the developers!")
		print("ERR - Parsed file couldn't find _fields_")
		return fields_extracted
	if not isinstance(all_nodes[1], ast.List):
		print("ERR - Bad parsing in py files! Something has changed. Contact the developers!")
		return fields_extracted

	fields = list(all_nodes[1].elts)
	fields_extracted = extract_py_fields(fields)
	return fields_extracted


def get_py_fields(filename):
	"""
	return py fields
	"""

	filename = os.path.join(PYTHON_DIR, filename)
	try:
		with open(filename, "r", encoding="utf-8") as py_file:
			node = ast.parse(py_file.read())
	except FileNotFoundError:
		sys.exit(
			"ERR - " + filename + " was not found at " + PYTHON_DIR + " -- Exiting Script"
		)
		return []

	class_definitions = [n for n in node.body if isinstance(n, ast.ClassDef)]

	if len(class_definitions) == 1:
		# print(">>>>> INFO - Class name detected: ", class_definitions[0].name)
		if len(class_definitions[0].body) != 2:
			print("ERR: Bad parsong! Something has changed. Contact the developers!")
			return []
		return extract_py_node(class_definitions[0].body[1])
	print("ERR: Bad parsing in py files! Something has changed. Contact the developers!")
	return []


def extract_c_fields(structs):
	"""
	return c fields
	"""
	fields_extracted = []
	# Initial validation
	if not isinstance(structs, dict) or len(structs) != 1:
		print(
			"ERR: - Incorrect object passed for extracting C fields. Contact developer team."
		)
		return fields_extracted

	value = list(structs.values())[0]
	if not isinstance(value, pyclibrary.c_parser.Struct):
		print(
			"ERR: - Incorrect object passed for extracting C fields. Contact developer team."
		)
		return fields_extracted

	fields_extracted = [each_field[0] for each_field in value.members]
	fields_extracted = [
		each_field
		for each_field in fields_extracted
		if not each_field.endswith("systemTime")
		if not each_field.endswith("deviceData")
	]

	return fields_extracted


def get_c_fields(name):
	"""
	get c fields
	"""
	filename = os.path.join(C_STRUCTS_DIR, name)
	if not os.path.isfile(filename):
		print("ERR - Could not find file", filename)
		return []
	parser = pyclibrary.CParser(process_all=False)
	try:
		file = parser.load_file(filename)
		if not file:
			print("ERR - Could not load file")
			return []
		parser.remove_comments(filename)
		parser.preprocess(filename)
		parser.parse_defs(filename)
		structs = parser.defs["structs"]
	except Exception as err:  # pylint: disable=broad-except
		print(f"ERR - File not found: {err}")
		return []

	return extract_c_fields(structs)


def validate_struct_files(python_file, c_struct_file):
	"""
	Validate c structs
	"""

	print("-" * 79)
	print(">>>>> INFO - Attempting Validation for filenames: ", python_file, c_struct_file)
	py_fields = get_py_fields(python_file)
	py_fields = sorted(py_fields, key=str.casefold)
	c_fields = get_c_fields(c_struct_file)
	c_fields = sorted(c_fields, key=str.casefold)
	matching_fields = set(py_fields) & set(c_fields)
	if len(py_fields) == len(c_fields):
		print(">>> Success! Number of fields were the same!")
	else:
		print(">>> Valiation failure! Number of fields differ!")
		input("Press enter to continue...")
		return
	if len(py_fields) == len(matching_fields) == len(c_fields):
		print(">>> Hooray! Validations successful!")
		print("-" * 79)
		return
	print(">>> Validation failure! Mismatch in fields!")
	input("Press enter to continue...")
	print("-" * 79)
	return


def main():
	"""Read py-c config and validate structs"""
	signal(SIGINT, sig_handler)  # Handle Ctrl-C or SIGINT

	print(
		"\n>>> Actuator Package Python Demo Scripts : Validates Python and C structs.<<<"
	)
	if len(sys.argv) > 2:
		sys.exit(
			"\nERR - Invalid arguments."
			+ "\n>>> Usage: python fxStructsValidatePy-C.py all"
			+ "\n>>>        python fxStructsValidatePy-C.py"
		)

	if len(sys.argv) == 1 or sys.argv[1] == "all":
		try:
			# read fields
			with open(COMPARE_FILE, "r", encoding="utf-8") as compare_file:
				lines = compare_file.readlines()
			for line in lines:
				py_file = line.split(",")[0].strip()
				c_struct_file = line.split(",")[1].strip()
				validate_struct_files(py_file, c_struct_file)
		except FileNotFoundError:
			sys.exit("ERR: " + COMPARE_FILE + " was not found at -- Exiting Script")
	else:
		print(">>> ERR: Bad Argument. ")
		sys.exit(
			"\nERR - Invalid arguments."
			+ "\n>>> Usage: python fxStructsValidatePy-C.py all"
			+ "\n>>>        python fxStructsValidatePy-C.py"
		)


if __name__ == "__main__":
	main()
