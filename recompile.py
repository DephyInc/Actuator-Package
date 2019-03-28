import os, sys, subprocess

isWindows = os.name == 'nt'
is_64bits = sys.maxsize > 2**32

original_dir = os.getcwd()
slash = '\\' if isWindows else '/'
platformdir = '/win' if isWindows else '/unix'
if is_64bits:
	platformdir = platformdir + '64'

platformdir = platformdir.replace('/', '\\')
stack_build_dir = original_dir + '/fx_plan_stack/build'
cscript_build_dir = original_dir + '/acpac_cscripts/build'

path_to_dll = original_dir + '/fx_plan_stack/build/libs/libfx_plan_stack.dll'

makeCmd = 'make'

if(isWindows):
	stack_build_dir = stack_build_dir.replace('/', '\\')
	cscript_build_dir = cscript_build_dir.replace('/', '\\')
	path_to_dll = path_to_dll.replace('/', '\\')
	makeCmd = 'mingw32-make -j'

print(stack_build_dir)

os.chdir(stack_build_dir)
os.system('cmake .. -DCOMPILE_SHARED=ON')
os.system(makeCmd)

copycmd = 'copy "' + path_to_dll + '" "' + cscript_build_dir + '"'
print("Executing:: " + copycmd)
os.system(copycmd)

os.chdir(cscript_build_dir)
os.system('cmake .. -G "MinGW Makefiles"')
os.system(makeCmd)
