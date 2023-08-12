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

def backup_build_dir():
	with tarfile.open('../../backup.tar.gz', 'w:gz') as tar:
		tar.add("..", arcname=os.path.basename(os.getcwd()))

def clean_build_dir(all_files=False):
	if all_files:
		subprocess.check_call(["mv", "tests/test1/test", ".."])
	shutil.rmtree("command-helper")
	shutil.rmtree("run-time-execute")
	shutil.rmtree("tests")
	if all_files:
		os.makedirs("tests/test1")
		subprocess.check_call(["mv", "../test", "tests/test1/"])

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
	_sleep_helper(0.075) ; print(".", end="", flush=True)
	_sleep_helper(0.05) ; print(".", end="", flush=True)
	_sleep_helper(0.025) ; print(".", end="", flush=True)
	print() ; _sleep_helper(0.2)

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
	except AttributeError:
		pass

	if not os.path.basename(os.getcwd()) == "source":
		print_info("not in source directory, exiting")
		exit(1)

	os.chdir("..")

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
			if not os.path.isfile(name):
				print_info("file {} does not exist, exiting".format(name))
				exit(1)
		elif type == "dir":
			if not os.path.isdir(name):
				print_info("directory {} does not exist, exiting".format(name))
				exit(1)

	os.makedirs(f"{BUILD_DIR}/command-helper", exist_ok=True)
	os.makedirs(f"{BUILD_DIR}/run-time-execute", exist_ok=True)
	os.makedirs(f"{BUILD_DIR}/tests/test1", exist_ok=True)

	os.chdir(BUILD_DIR)

	if args.command == "build":
		def compile_candidate(name, commands):
			print_info(f"compiling {name}")
			if commands[0] == "gcc": commands = [commands[0]] + GCC_ARGS + commands[1:]
			if commands[0] == "!gcc": commands = ["gcc"] + commands[1:]
			subprocess.check_call(commands)
			print("\n\n")
		
		compile_candidate("command-helper", ["gcc", "-c", "../source/command-helper/command-helper.c", "-o", "command-helper/command-helper.o"])
		compile_candidate("run-time-execute", ["gcc", "-c", "../source/run-time-execute/run-time-execute.c", "-o", "run-time-execute/run-time-execute.o"])
		compile_candidate("run-time-execute", ["ar", "rcs", "run-time-execute/librun-time-execute.a", "run-time-execute/run-time-execute.o", "command-helper/command-helper.o"])
		compile_candidate("test1", ["gcc", "-c", "../source/tests/test1/test.c", "-o", "tests/test1/test.o"])
		compile_candidate("test1", ["!gcc", "tests/test1/test.o", "-o", "tests/test1/test", "-Lrun-time-execute", "-lrun-time-execute"])

	elif args.command == "clean":
		do_remove_all = None
		if args.all:
			do_remove_all = True
		backup_build_dir()
		clean_build_dir(do_remove_all)

if __name__ == "__main__":
 	main()