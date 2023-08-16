import subprocess
import argparse
import tarfile
import shutil
import time
import os

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
	if seconds > 0: time.sleep(seconds * info_delay_multiplier)

def print_info(*args, **kwargs):
	if "end" not in kwargs:
		kwargs['end'] = ""
	if "flush" not in kwargs:
		kwargs['flush'] = True
	print(*args, **kwargs)
	_sleep_helper(0.075) ; print(".", end=kwargs["end"], flush=kwargs['flush'])
	_sleep_helper(0.05) ; print(".", end=kwargs["end"], flush=kwargs['flush'])
	_sleep_helper(0.025) ; print(".", end=kwargs["end"], flush=kwargs['flush'])
	print() ; _sleep_helper(0.2)

def compile_candidate(name, commands):
	print_info(f"Compiling, [{name}]")
	if commands[0] == "gcc": commands = [commands[0]] + GCC_ARGS + commands[1:]
	if commands[0] == "!gcc": commands = ["gcc"] + commands[1:]
	subprocess.check_call(commands)
	print("\n\n")

def main():
	global info_delay_multiplier

	parser = argparse.ArgumentParser(description="Build the project.")
	sub_parsers = parser.add_subparsers(help="sub-commands:", dest="command")

	common_args = argparse.ArgumentParser(add_help=False)
	common_args.add_argument("-d", "--delay-multiplier", type=float, default=1, help="Delay multiplier for printing status.")
	common_args.add_argument("-v", "--verbose", action="store_true", help="Print more information.")

	build_parser = sub_parsers.add_parser("build", help="Build the project.", parents=[common_args])
	build_parser.add_argument("-c", "--clean", action="store_true", help="Clean the build directory before building [default=true].")
	build_parser.add_argument("-n", "--no-backup", action="store_true", help="Do not backup the build directory before cleaning it.")
	build_parser.add_argument("-b", "--backup-location", type=str, help="Backup location. Must specify if backing up.")

	clean_parser = sub_parsers.add_parser("clean", help="Remove the leftovers from the build process.", parents=[common_args])
	clean_parser.add_argument("-a", "--all", action="store_true", help="Remove all the build files, including the executables.")

	backup_parser = sub_parsers.add_parser("backup", help="Backup the build directory.", parents=[common_args])
	backup_parser.add_argument("-b", "--backup-location", required=True, type=str, help="Backup location.")

	args = parser.parse_args()

	# TODO: is this try.except block really necessary?
	try:
		info_delay_multiplier = args.delay_multiplier
	except AttributeError:
		pass

	if args.verbose: print_info("Checking that we are in the right directory")
	if not os.path.basename(os.getcwd()) == "source":
		print_info("Not in source directory, exiting")
		exit(1)

	if args.verbose: print_info("Moving to the root directory")
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

	if args.verbose: print_info("Performing sanity checks")
	for check in checks:
		type, name = check
		if type == "file" and not os.path.isfile(name):
			print_info(f"File, [{name}], does not exist, exiting")
			exit(1)
		elif type == "dir" and not os.path.isdir(name):
			print_info(f"Directory, [{name}], does not exist, exiting")
			exit(1)
		else:
			raise Exception(f"Invalid check type: [{type}]")

	if args.verbose: print_info("Making sure the build dirs exist")
	os.makedirs("built/command-helper", exist_ok=True)
	os.makedirs("built/run-time-execute", exist_ok=True)
	os.makedirs("built/tests/test1", exist_ok=True)


	if args.command == "build":
		if args.verbose: print_info("Moving to the build directory")
		os.chdir("built")
		compile_candidate("command-helper", ["gcc", "-c", "../source/command-helper/command-helper.c", "-o", "command-helper/command-helper.o"])
		compile_candidate("run-time-execute", ["gcc", "-c", "../source/run-time-execute/run-time-execute.c", "-o", "run-time-execute/run-time-execute.o"])
		compile_candidate("run-time-execute", ["ar", "rcs", "run-time-execute/librun-time-execute.a", "run-time-execute/run-time-execute.o", "command-helper/command-helper.o"])
		compile_candidate("test1:pre", ["gcc", "-c", "../source/tests/test1/test.c", "-o", "tests/test1/test.o"])
		compile_candidate("test1", ["!gcc", "tests/test1/test.o", "-o", "tests/test1/test", "-Lrun-time-execute", "-lrun-time-execute"])
		if args.verbose: print_info("Moving back to the root directory")
		os.chdir("..")

	elif args.command == "clean":
		do_remove_all = None
		if args.all: do_remove_all = True
		backup_build_dir()
		clean_build_dir(do_remove_all)
	
	elif args.command == "backup":
		backup_build_dir()
	
	print_info("[ Done, enjoy your day coding :D ]")


if __name__ == "__main__":
 	main()