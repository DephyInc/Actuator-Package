from signal import signal, SIGINT
import os
import sys
import pandas
import ast
import pyclibrary
import inspect

C_STRUCTS_DIR = os.path.join(os.getcwd(),"..","inc")
PYTHON_DIR = os.path.join(os.getcwd(),"flexseapython", "dev_spec")
SPECS_DIR = os.path.join(os.getcwd(),"..", "..", "flexsea-core","flexsea-system", "device_specs_csv")
IGNORE_FILES = ['__init__.py', '__pycache__', 'AllDevices.py']


def sig_handler(frame, signal_received):
    return sys.exit('\nCTRL-C or SIGINT detected\nExiting ...')

def find_files(file_path, ignore_list, strip_characters):
    #Filter only files that we are concerned with. Endswith: *State.py
    files_found = [file for file in os.listdir(file_path)
                    if file not in ignore_list
                    if file.endswith(strip_characters)]
    #strip filenames
    files_found = [file[:-len(strip_characters)] for file in files_found]
    return files_found

def get_spec_fields(filename):
    filename = os.path.join(SPECS_DIR,filename)
    print("\n>>> IN-PROCESS - Extracting fields from spec CSV file: " + filename)
    fields = []
    try:
        # read fields
        with open(filename) as spec_file:
            fields = pandas.read_csv(filename, usecols=[0])[1:]
    except FileNotFoundError as e:
        sys.exit("ERR - " + filename + " was not found at " + SPECS_DIR + " -- Exiting Script")

    #formatting name for accommodation of variation if field names in python and c structs
    spec_fields = [field.replace('[', r'_').replace(']', r'_').replace('.', r'').lower() for field in
              list(fields.variable_label)]
    return spec_fields


def extract_py_fields(ast_fields):
    fields = []
    for each_tup in ast_fields:
        fields.append(each_tup.elts[0].s)
    fields = [field for field in fields
              if not field.endswith("SystemTime")]
    return fields

def extract_py_node(classNode):
    all_nodes = [node for node in ast.iter_child_nodes(classNode)]
    fields_extracted = []
    if len(all_nodes) != 2:
        print("ERR: Bad parsing in py files! Something has changed. Contact the developers!")
        return
    if not (isinstance(all_nodes[0], ast.Name) and all_nodes[0].id == "_fields_"):
        print("ERR - Bad parsing in py files! Something has changed. Contact the developers!")
        print("ERR - Parsed file couldn't find _fields_")
        return
    if not isinstance(all_nodes[1], ast.List):
        print("ERR - Bad parsing in py files! Something has changed. Contact the developers!")
        return
    else:
        fields = [e for e in all_nodes[1].elts]
        fields_extracted = extract_py_fields(fields)
    return fields_extracted

def get_py_fields(filename):
    filename = os.path.join(PYTHON_DIR,filename)
    print("\n>>> IN-PROCESS - Extracting fields from python state file: " + filename)
    try:
        with open(filename) as py_file:
            node = ast.parse(py_file.read())
    except FileNotFoundError as e:
        sys.exit("ERR - " + filename + " was not found at " + SPECS_DIR + " -- Exiting Script")
        return

    class_definitions = [n for n in node.body if isinstance(n, ast.ClassDef)]

    if len(class_definitions) == 1:
        print(">>>>> INFO - Class name detected: ", class_definitions[0].name)
        if len(class_definitions[0].body) != 2:
            print("ERR: Bad parsong! Something has changed. Contact the developers!")
            return
        else:
            return extract_py_node(class_definitions[0].body[1])
    else:
        print("ERR: Bad parsing in py files! Something has changed. Contact the developers!")
        return


def extract_c_fields(structs):
    fields_extracted = []
    #Initial validation
    if not isinstance(structs, dict) or len(structs) != 1:
        print("ERR: - Incorrect object passed for extracting C fields. Contact developer team.")
        return

    key= list(structs)[0]
    value = list(structs.values())[0]
    #print('----------\nKEY: ', key)#, '\nVALUE: ', value,"\n----------")
    #print('----------\nKEY-TYPE: ', type(key), '\nVALUE-TYPE: ', type(value), "\n----------")
    if not isinstance(value, pyclibrary.c_parser.Struct):
        print("ERR: - Incorrect object passed for extracting C fields. Contact developer team.")
        return

    #print(">>>>> DEBUG - c_parser.Struct detected! Number of fields before processing: ", len(value.members))

    fields_extracted = [each_field[0] for each_field in value.members]
    fields_extracted = [each_field for each_field in fields_extracted
                        if not each_field.endswith("systemTime")
                        if not each_field.endswith("deviceData")]

    return fields_extracted

def get_c_fields(filename):
    filename = os.path.join(C_STRUCTS_DIR,filename)
    print("\n>>> IN-PROCESS - Extracting fields from c struct file: " + filename)
    parser = pyclibrary.CParser(process_all=False)
    fields = []
    fields_extracted = []
    try:
        fl = parser.load_file(filename)
        if not fl :
            print("ERR - Could not load file")
            return
        parser.remove_comments(filename)
        parser.preprocess(filename)
        parser.parse_defs(filename)
        structs = parser.defs['structs']
    except:
        print("ERR - File not found")
        return

    return extract_c_fields(structs)


def validate_struct_files(filename_pairs):
    """print ("Python file: " + os.path.join(PYTHON_DIR,filename_pairs[0]))
    print ("C file: " + os.path.join(C_STRUCTS_DIR,filename_pairs[1]))
    print ("Spec file: " + os.path.join(SPECS_DIR,filename_pairs[2]))"""
    print("-----------------------------------------------------------------------------")
    print(">>>>> INFO - Attempting Validation for filenames: ", *filename_pairs)
    spec_fields = get_spec_fields(filename_pairs[2])
    spec_fields = sorted(spec_fields, key=str.casefold)
    print(">>>>> INFO - ", len(spec_fields), " Fields extracted")
    print(">>>>> INFO - Fields: ", *spec_fields)
    py_fields = get_py_fields(filename_pairs[0])
    py_fields = sorted(py_fields, key=str.casefold)
    print(">>>>> INFO - ", len(py_fields), " Fields extracted")
    print(">>>>> INFO - Fields: ", *py_fields)
    c_fields = get_c_fields(filename_pairs[1])
    c_fields = sorted(c_fields, key=str.casefold)
    print(">>>>> INFO - ", len(c_fields), " Fields extracted")
    print(">>>>> INFO - Fields: ", *c_fields)
    matching_fields = set(spec_fields) & set(py_fields) & set(c_fields)
    print(">>>>> INFO - ", len(matching_fields), " fields were found in common!")
    if len(spec_fields) == len(py_fields)\
        and len(spec_fields) == len(c_fields):
        print(">>> VALIDATION(1) SUCCESS - Good news. Length validation of fields in spec, struct and python class files were successful. That is all three files have the same number of fields!")
    else:
        print(">>> VALIDATION(1) FAILURE - Bad news. Complete validation was not successful")
    if len(spec_fields) == len(matching_fields):
        print(">>> VALIDATION(2) SUCCESS - Good news. All fields are matching in all three files!")
    else:
        print(">>> VALIDATION(2) FAILURE - Bad news. Field validation error. Could not validate individual field")
    print("-----------------------------------------------------------------------------")
    return

if __name__ == '__main__':
    signal(SIGINT, sig_handler)	# Handle Ctrl-C or SIGINT

    print('\n>>> Actuator Package Python Demo Scripts : Validates Python and C structs.<<<')
    if len(sys.argv)!= 2:
        sys.exit("\nERR - Invalid arguments."+ \
                 "\n>>> Usage: python fxStructsValidatePy-C.py all" + \
                 "\n>>>        python fxStructsValidatePy-C.py ActPack" +\
                 "\n>>>        python fxStructsValidatePy-C.py BMS" )

    if sys.argv[1] == "all":
        #find all files
        all_python_files = find_files(PYTHON_DIR, IGNORE_FILES, "State.py")
        all_c_files = find_files(C_STRUCTS_DIR, IGNORE_FILES, "_struct.h")
        all_spec_files = find_files(SPECS_DIR, IGNORE_FILES, "_specs.csv")
        #find matching file names
        files_w_matching_names = set([file.lower() for file in all_python_files]) &\
                                 set([file.lower() for file in all_c_files]) &\
                                 set([file.lower() for file in all_spec_files])
        #Remove non matching file names from the list
        all_python_files = [file for file in all_python_files
                            if file.lower() in files_w_matching_names]
        all_c_files = [file for file in all_c_files
                       if file.lower() in files_w_matching_names]
        all_spec_files = [file for file in all_spec_files
                       if file.lower() in files_w_matching_names]
        #sort the filenames
        python_files = sorted(all_python_files, key=str.casefold)
        c_files = sorted(all_c_files, key=str.casefold)
        spec_files = sorted(all_spec_files, key=str.casefold)
        #At this point the list is exactly how we want. So reformat it as required
        all_python_files = [file + "State.py" for file in python_files]
        all_c_files = [file + "_struct.h" for file in c_files]
        all_spec_files = [file + "_specs.csv" for file in spec_files]

        #create pairs of filenames that need to eb validated
        matching_filename_pairs = list(zip(all_python_files,all_c_files,all_spec_files))
        print("\n>>> INFO: " + str(len(files_w_matching_names)) + " Pairs of matching file(s) found:\n")
        #print(*matching_filename_pairs)
        for filename_pairs in matching_filename_pairs:
            validate_struct_files(filename_pairs)


    else:
        #validate single struct file
        all_python_files = find_files(PYTHON_DIR, IGNORE_FILES, "State.py")
        all_c_files = find_files(C_STRUCTS_DIR, IGNORE_FILES, "_struct.h")
        all_spec_files = find_files(SPECS_DIR, IGNORE_FILES, "_specs.csv")
        if sys.argv[1].lower() in [file.lower() for file in all_python_files] and \
            sys.argv[1].lower() in [file.lower() for file in all_c_files]:
            filename_py = [file for file in all_python_files
                           if file.lower() == sys.argv[1].lower()][0]
            filename_c = [file for file in all_c_files
                           if file.lower() == sys.argv[1].lower()][0]
            filename_spec = [file for file in all_spec_files
                          if file.lower() == sys.argv[1].lower()][0]
            print("\n>>> INFO: Matching struct file found for: " )
            filename_pairs = (filename_py + "State.py", filename_c + "_struct.h", filename_spec + "_specs.csv")
            #print(*filename_pairs)
            validate_struct_files(filename_pairs)
