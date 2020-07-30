from signal import signal, SIGINT
import os
import sys

C_STRUCTS_DIR = os.path.join(os.getcwd(),"..","inc")
PYTHON_DIR = os.path.join(os.getcwd(),"flexseapython", "dev_spec")
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

def validate_struct_files(filename_python, filename_c):
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
        all_python_files = find_files(PYTHON_DIR, IGNORE_FILES, "State.py")
        all_c_files = find_files(C_STRUCTS_DIR, IGNORE_FILES, "_struct.h")
        files_w_matching_names = set([file.lower() for file in all_python_files]) &\
                                 set([file.lower() for file in all_c_files])
        print("\n>>> INFO: Validating " + str(len(files_w_matching_names)) + \
              " struct file(s): " )
        print(*files_w_matching_names, sep="\t")
        """for struct_file in files_w_matching_names:
            validate_struct_files(struct_file)"""


    else:
        #validate single struct file
        print("\n>>> INFO: Validating struct file(s): " + sys.argv[1])
        #validate_struct_files(sys.argv[1])



