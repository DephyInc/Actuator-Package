from signal import signal, SIGINT
import os
import sys

def sig_handler(frame, signal_received):
    return sys.exit('\nCTRL-C or SIGINT detected\nExiting ...')

def get_py_structs():
    return

def get_c_structs():
    return

def get_matching_struct_files(python_struct_files, c_struct_files):
    return

def validate_struct_files(struct_filename):
    return


if __name__ == '__main__':
    signal(SIGINT, sig_handler)	# Handle Ctrl-C or SIGINT

    print('\n>>> Actuator Package Python Demo Scripts : Validates Python and C structs.<<<'+\
          "\n>>> It only validates the fields of the structs")
    list_of_structs_to_compare = []

    if len(sys.argv)!= 2:
        sys.exit("\n>>> ERR: Invalid arguments."+ \
                 "\n>>> Usage: python fxStructsValidatePy-C.py all" + \
                 "\n>>>        python fxStructsValidatePy-C.py ActPack" +\
                 "\n>>>        python fxStructsValidatePy-C.py BMS" )

    if sys.argv[1] == "all":
        #Validate all files
        #all_specs = next(os.walk())[2]
        all_python_struct_files = get_py_structs()
        all_c_struct_files = get_c_structs()
        struct_files_w_matching_names = get_matching_struct_files(all_python_struct_files, all_c_struct_files)
        print("\n>>> INFO: Validating struct file(s): " + struct_files_w_matching_names)
        for struct_file in struct_files_w_matching_names:
            validate_struct_files(struct_file)


    else:
        #validate single struct file
        print("\n>>> INFO: Validating struct file(s): " + sys.argv[1])
        validate_struct_files(argv[1])



