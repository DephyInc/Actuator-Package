import os, subprocess

original_dir = os.getcwd()

stack_build_dir = original_dir + '/fx_plan_stack/build'
cscript_build_dir = original_dir + '/acpac_cscripts/build'
path_to_dll = original_dir + '/fx_plan_stack/build' + '/libfx_plan_stack.dll'
makeCmd = 'make'

isWindows = os.name == 'nt'

if(isWindows):
	stack_build_dir = stack_build_dir.replace('/', '\\')
	cscript_build_dir = cscript_build_dir.replace('/', '\\')
	path_to_dll = path_to_dll.replace('/', '\\')
	makeCmd = 'mingw32-make'

print(stack_build_dir)

os.chdir(stack_build_dir)
os.system('cmake .. -DCOMPILE_SHARED=ON')
os.system(makeCmd)

copycmd = 'copy "' + path_to_dll + '" "' + cscript_build_dir + '"'
print("Executing:: " + copycmd)
os.system(copycmd)

os.chdir(cscript_build_dir)
os.system('cmake ..')
os.system(makeCmd)
