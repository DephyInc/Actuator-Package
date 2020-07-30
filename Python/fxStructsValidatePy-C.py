from signal import signal, SIGINT
import os
import sys
import pandas

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

def get_py_fields(filename):
    filename = os.path.join(SPECS_DIR,filename)
    print("\n>>> IN-PROCESS: Extracting fields from python state file: " + filename)
    return

def get_spec_fields(filename):
    filename = os.path.join(SPECS_DIR,filename)
    print("\n>>> IN-PROCESS: Extracting fields from spec CSV file: " + filename)
    fields = []
    try:
        # read fields
        with open(filename) as spec_file:
            fields = pandas.read_csv(filename, usecols=[0])[1:]
    except FileNotFoundError as e:
        sys.exit("ERR: " + filename + " was not found at " + SPECS_DIR + " -- Exiting Script")
    print("\n>>> INFO: " + str(len(list(fields.variable_label))) + " Fields detected in " + filename + ": ")
    print(*fields.variable_label, sep=", ")
    return list(fields.variable_label)

def get_c_fields(filename):
    filename = os.path.join(SPECS_DIR,filename)
    print("\n>>> IN-PROCESS: Extracting fields from c struct file: " + filename)
    return


def validate_struct_files(filename_pairs):
    """print ("Python file: " + os.path.join(PYTHON_DIR,filename_pairs[0]))
    print ("C file: " + os.path.join(C_STRUCTS_DIR,filename_pairs[1]))
    print ("Spec file: " + os.path.join(SPECS_DIR,filename_pairs[2]))"""
    py_fields = get_py_fields(filename_pairs[0])
    c_fields = get_c_fields(filename_pairs[1])
    spec_fields = get_spec_fields(filename_pairs[2])
    return

if __name__ == '__main__':
    signal(SIGINT, sig_handler)	# Handle Ctrl-C or SIGINT

    print('\n>>> Actuator Package Python Demo Scripts : Validates Python and C structs.<<<')
    if len(sys.argv)!= 2:
        sys.exit("\n>>> ERR: Invalid arguments."+ \
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
        print(*matching_filename_pairs)
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
            print(*filename_pairs)
            validate_struct_files(filename_pairs)
