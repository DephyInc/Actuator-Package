from signal import signal, SIGINT
import os
import sys

C_STRUCTS_DIR = os.path.join(os.getcwd(),"..","inc")
PYTHON_DIR = os.path.join(os.getcwd(),"flexseapython", "dev_spec")
IGNORE_FILES = ['__init__.py', '__pycache__', 'AllDevices.py']

def sig_handler(frame, signal_received):
    return sys.exit('\nCTRL-C or SIGINT detected\nExiting ...')

def get_py_structs():
    #Filter only files that we are concerned with. Endswith: *State.py
    all_py_files = [file for file in os.listdir(PYTHON_DIR)
                    if file not in IGNORE_FILES
                    if file.endswith("State.py")]
    print ("\n>>> INFO: " + str(len(all_py_files)) + \
           " Python State file(s) detected at " + PYTHON_DIR + ":")
    print(*all_py_files, sep=", ")
    return

def get_c_structs():
    #Filter only files that we are concerned with. Endswith: *struct.h
    all_c_files = [file for file in os.listdir(C_STRUCTS_DIR)
                   if file.endswith("struct.h")]
    print ("\n>>> INFO: " + str(len(all_c_files)) + \
           " C struct file(s) detected at " + C_STRUCTS_DIR+ ":")
    print(*all_c_files, sep=", ")
    return

def get_matching_struct_files(python_struct_files, c_struct_files):
    return

def validate_struct_files(struct_filename):
    return


if __name__ == '__main__':
    signal(SIGINT, sig_handler)	# Handle Ctrl-C or SIGINT

    print('\n>>> Actuator Package Python Demo Scripts : Validates Python and C structs.<<<'+\
          "\n>>> It only validates the fields of the structs")

    if len(sys.argv)!= 2:
        sys.exit("\n>>> ERR: Invalid arguments."+ \
                 "\n>>> Usage: python fxStructsValidatePy-C.py all" + \
                 "\n>>>        python fxStructsValidatePy-C.py ActPack" +\
                 "\n>>>        python fxStructsValidatePy-C.py BMS" )

    if sys.argv[1] == "all":
        all_python_files = get_py_structs()
        all_c_files = get_c_structs()
        files_w_matching_names = get_matching_struct_files(all_python_files, all_c_files)
        """print("\n>>> INFO: Validating struct file(s): " + files_w_matching_names)
        for struct_file in files_w_matching_names:
            validate_struct_files(struct_file)"""


    else:
        #validate single struct file
        print("\n>>> INFO: Validating struct file(s): " + sys.argv[1])
        #validate_struct_files(sys.argv[1])



