import subprocess
import argparse
import tarfile
import shutil
import time
import os

BUILD_DIR = 'built'
SOURCE_DIR = 'source'
GCC_ARGS = [
	"-Wall", "-Wextra", "-Wshadow", "-Wconversion", "-Wuninitialized", "-Wunused",
	"-Wstrict-prototypes", "-Wcast-align", "-Wformat-security",
	"-Wdangling-else", "-Wdouble-promotion", "-Wformat=2", "-O3"
]
COMPILER = ["gcc"] + GCC_ARGS

def compile_file(input_file, output_file):
	cmd = COMPILER + ['-c', input_file, '-o', output_file]
	subprocess.check_call(cmd)

def link_files(input_files, output_file, libs=[]):
	cmd = COMPILER + input_files + ['-o', output_file]
	for lib in libs:
		cmd += ['-L' + os.path.dirname(lib), '-l' + os.path.basename(lib).split('lib')[1].split('.')[0]]
	subprocess.check_call(cmd)

def backup_build_dir():
	os.chdir('..')
	with tarfile.open('../backup.tar.gz', 'w:gz') as tar:
		tar.add(BUILD_DIR)

def clean_build_dir():
	shutil.rmtree(BUILD_DIR)

def build():
	compile_file(
		os.path.join("..", SOURCE_DIR, 'command-helper', 'command-helper.c'),
		os.path.join('command-helper', 'command-helper.o')
	)

	compile_file(
		os.path.join("..", SOURCE_DIR, 'run-time-execute', 'run-time-execute.c'),
		os.path.join('run-time-execute', 'run-time-execute.o')
	)

	with open(os.path.join('run-time-execute', 'librun-time-execute.a'), 'wb') as f:
		subprocess.check_call([
			'ar', 'rcs', f.name,
			os.path.join('run-time-execute', 'run-time-execute.o'),
			os.path.join('command-helper', 'command-helper.o')
		])

	compile_file(
		os.path.join("..", SOURCE_DIR, 'tests', 'test1', 'test.c'),
		os.path.join('tests', 'test1', 'test1.o')
	)
	
	link_files(
		[os.path.join('tests', 'test1', 'test.o')],
		os.path.join('tests', 'test1', 'test'),
		libs=[os.path.join('run-time-execute', 'librun-time-execute.a')]
	)

info_delay_multiplier = 1
def _sleep_helper(seconds):
	if seconds > 0:
		time.sleep(seconds * info_delay_multiplier)

def print_info(*args, **kwargs):
	if "end" not in kwargs:
		kwargs['end'] = ""
	if "flush" not in kwargs:
		kwargs['flush'] = True
	print(*args, **kwargs)
	_sleep_helper(0.2) ; print(".", end="", flush=True)
	_sleep_helper(0.2) ; print(".", end="", flush=True)
	_sleep_helper(0.2) ; print(".", end="", flush=True)
	print() ; _sleep_helper(0.1)

def main():
	global info_delay_multiplier

	parser = argparse.ArgumentParser(description="Build the project.")
	sub_parsers = parser.add_subparsers(help="sub-commands:", dest="command")

	common_args = argparse.ArgumentParser(add_help=False)
	common_args.add_argument("-d", "--delay-multiplier", type=float, default=1, help="Delay multiplier for printing status.")

	build_parser = sub_parsers.add_parser("build", help="Build the project.", parents=[common_args])
	clean_parser = sub_parsers.add_parser("clean", help="Remove the leftovers from the build process.", parents=[common_args])

	clean_parser.add_argument("-a", "--all", action="store_true", help="Remove all the build files, including the executables.")

	args = parser.parse_args()

	try:
		info_delay_multiplier = args.delay_multiplier
	except AttributeError: pass

	print_info("checking we are executing from the correct directory")
	if not os.path.basename(os.getcwd()) == "source":
		print_info("not in source directory, exiting")
		exit(1)

	os.chdir("..")

	print_info("checking that all the required files and directories exist")

	checks = [
		["file", "LICENSE"],
		["file", "README.md"],
		["file", "TODO.md"],

		["dir", "source"],
		["dir", "source/command-helper"],
		["dir", "source/execution-helper"],
		["dir", "source/run-time-execute"],
		["dir", "source/tests"],
		["dir", "source/tests/test1"],

		["file", "source/command-helper/command-helper.h"],
		["file", "source/command-helper/command-helper.c"],
		["file", "source/execution-helper/execution-helper.h"],
		["file", "source/run-time-execute/run-time-execute.h"],
		["file", "source/run-time-execute/run-time-execute.c"],
		["file", "source/tests/test1/test.c"],
		["file", "source/tests/test1/run-time-target.c"],
	]

	for check in checks:
		type, name = check
		if type == "file":
			dir_change = name.split("/")
			back_num = 0
			if len(dir_change) > 1:
				for dir in dir_change[:-1]:
					os.chdir(f"./{dir}")
					back_num += 1
			name = dir_change[-1]
			if not name in os.listdir("."):
				print_info("file {} does not exist, exiting".format(name))
				exit(1)
			if not os.path.isfile(name):
				print_info("{} is not a file, exiting".format(name))
				exit(1)
			for _ in range(back_num):
				os.chdir("..")
		elif type == "dir":
			dir_change = name.split("/")
			back_num = 0
			if len(dir_change) > 1:
				for dir in dir_change[:-1]:
					os.chdir(f"./{dir}")
					back_num += 1
			name = dir_change[-1]
			if not name in os.listdir("."):
				print_info("directory {} does not exist, exiting".format(name))
				exit(1)
			if not os.path.isdir(name):
				print_info("{} is not a directory, exiting".format(name))
				exit(1)
			for _ in range(back_num):
				os.chdir("..")
	
	if not os.path.exists(BUILD_DIR):
		print_info("build dir does not exist, creating it")
		os.makedirs(BUILD_DIR)
	
	if not os.path.isdir(os.path.join(BUILD_DIR, "command-helper")):
		print_info("command-helper dir does not exist, creating it")
		os.makedirs(os.path.join(BUILD_DIR, "command-helper"))
	
	if not os.path.isdir(os.path.join(BUILD_DIR, "run-time-execute")):
		print_info("run-time-execute dir does not exist, creating it")
		os.makedirs(os.path.join(BUILD_DIR, "run-time-execute"))
	
	if not os.path.isdir(os.path.join(BUILD_DIR, "tests")):
		print_info("tests dir does not exist, creating it")
		os.makedirs(os.path.join(BUILD_DIR, "tests"))
	
	if not os.path.isdir(os.path.join(BUILD_DIR, "tests", "test1")):
		print_info("tests/test1 dir does not exist, creating it")
		os.makedirs(os.path.join(BUILD_DIR, "tests", "test1"))
	
	os.chdir(BUILD_DIR)

	if args.command == "build":
		build()
	
	elif args.command == "clean":
		do_remove_all = None
		if args.all:
			do_remove_all = True
		backup_build_dir()
		clean_build_dir(do_remove_all)

if __name__ == "__main__":
	main()