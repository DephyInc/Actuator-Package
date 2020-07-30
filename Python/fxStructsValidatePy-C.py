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
    #strip filenames
    all_py_files = [file[:-8].lower() for file in all_py_files ]
    return all_py_files

def get_c_structs():
    #Filter only files that we are concerned with. Endswith: *struct.h
    all_c_files = [file for file in os.listdir(C_STRUCTS_DIR)
                   if file.endswith("_struct.h")]
    #Strip out "_struct.h" from the end of filename
    all_c_files = [file[:-9].lower() for file in all_c_files]
    return all_c_files

def validate_struct_files(struct_filename):
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
        all_python_files = get_py_structs()
        all_c_files = get_c_structs()
        files_w_matching_names = set(all_python_files) & set(all_c_files)
        print("\n>>> INFO: Validating " + str(len(files_w_matching_names)) + \
              " struct file(s): " )
        print(*files_w_matching_names, sep="\t")
        """for struct_file in files_w_matching_names:
            validate_struct_files(struct_file)"""


    else:
        #validate single struct file
        print("\n>>> INFO: Validating struct file(s): " + sys.argv[1])
        #validate_struct_files(sys.argv[1])



