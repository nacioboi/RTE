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

def clean_build_dir(verbose, all_files):
	if verbose: print_info("Moving to the build directory")
	os.chdir("built")
	print_info("Commencing clean for all files" if all_files else "Commencing clean")
	if not all_files:
		subprocess.check_call(["mv", "tests/test1/test", ".."])
	shutil.rmtree("command-helper")
	shutil.rmtree("run-time-execute")
	shutil.rmtree("tests")
	if not all_files:
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

class ArgumentsHolder:
	def assign(self, name, value):
		setattr(self, name, value)

def try_get_args(argument_holder, arg_list):
	for name, callback in arg_list:
		try:
			argument_holder.assign(name, callback())
		except:
			argument_holder.assign(name, None)

def main():
	global info_delay_multiplier

	parser = argparse.ArgumentParser(description="Build the project.")
	sub_parsers = parser.add_subparsers(help="sub-commands:", dest="command")

	common_args = argparse.ArgumentParser(add_help=False)
	common_args.add_argument("-D", "--delay-multiplier", type=float, default=1, help="Delay multiplier for printing status.")
	common_args.add_argument("-v", "--verbose", action="store_true", help="Print more information.")
	common_args.add_argument("-q", "--quiet", action="store_true", help="Only output to log file (if specified).")
	common_args.add_argument("--log-file", type=str, help="Log file location.")

	build_parser = sub_parsers.add_parser("build", help="Build the project.", parents=[common_args])
	build_parser.add_argument("-c", "--do-clean", action="store_true", help="Clean the build directory before building.")
	build_parser.add_argument("-b", "--do-backup", action="store_true", help="Backup the build directory before cleaning it.")
	build_parser.add_argument("-l", "--backup-location", type=str, help="Backup location. Must specify if backing up.")

	clean_parser = sub_parsers.add_parser("clean", help="Remove the leftovers from the build process.", parents=[common_args])
	clean_parser.add_argument("-a", "--all", action="store_true", help="Remove all the build files, including the executables.")

	backup_parser = sub_parsers.add_parser("backup", help="Backup the build directory.", parents=[common_args])
	backup_parser.add_argument("-l", "--backup-location", required=True, type=str, help="Backup location.")

	review_parser = sub_parsers.add_parser("review", help="Review the log file, this way you can better analyze the build process.",
								parents=[common_args])
	review_parser.add_argument("-i", "--interactive", action="store_true", help="Review the log file interactively.")
	_help_text = ""
	_help_text += "Date range to filter."
	_help_text += " [Format: YYYY/MM/DD-YYYY/MM/DD]."
	_help_text += " [E.G: 2023/04/21-2023/04/24]."
	review_parser.add_argument("-d", "--date-range", type=str, help=_help_text)
	_help_text = ""
	_help_text += "Time range to filter (in the context of --date-range, if specified, else the current day)."
	_help_text += " [Format: HH:MM:SS-HH:MM:SS]."
	_help_text += " [E.G: 12:00:00-13:00:00]."
	_help_text += " The hours are in 24-hour format, starting from the first day."
	_help_text += " See epilogue for more information."
	review_parser.add_argument("-t", "--time-range", type=str, help=_help_text)

	_epilog = ""
	_epilog += "On date and time filtering...\n"
	_epilog += "The date and times are inclusively calculated. Meaning that if you specify 2023/04/21-2023/04/24,"
	_epilog += " the date range will include the 1st day, 2nd day, 3rd day, and 4th day.\n"
	_epilog += "The same applies to the time range. If you specify 12:00:00-13:00:00, the time range will include"
	_epilog += " 12:00:00, 12:01:00, 12:02:00, ..., 12:59:00, 13:00:00.\n"
	_epilog += "You may not specify a single time range, you must specify both the start and end time.\n"
	_epilog += "You can however, specify a single date range, in which case, the time range will be the entire day.\n"
	_epilog += "The hours are in 24-hour format, starting from the first day with respect to the date range.\n"
	_epilog += "For example, if the date range is 2023/04/21-2023/04/24, and the time range is 12:00:00-13:00:00,"
	_epilog += " the time range will be 12:00:00-13:00:00 for only the first day, meaning then, that no other day"
	_epilog += " will have a time range specified.\n"
	_epilog += "Meaning still, that in this hypothetical scenario, the filter will forget about all the other days except"
	_epilog += " the first day, and will only filter the first day with the time range specified.\n"
	_epilog += "To include all the days, you must specify the time range with the postfix `*`.\n"
	_epilog += "For example, if the date range is 2023/04/21-2023/04/24, and the time range is 12:00:00-13:00:00*,"
	_epilog += " the time range will be 12:00:00-13:00:00 for all the days, meaning then, that all the days"
	_epilog += " will have a time range specified.\n"
	_epilog += "You may also specify to include hours overflowing to the subsequent days.\n"
	_epilog += "For example, if the date range is 2023/04/21-2023/04/24, and the time range is 12:00:00-60:00:00,"
	_epilog += " the time range will be 12:00:00-24:00:00 for the first day and 00:00:00-24:00:00 for the next two days.\n"
	_epilog += "To make life easier, you may use abbreviations for time ranges but not the date ranges.\n"
	_epilog += "For example, if the time range we want is 12:00:00-13:00:00, we may specify it as 12::-13::.\n"

	parser.epilog = _epilog

	_args = parser.parse_args()
	args = ArgumentsHolder()

	try_get_args(args, [
		["command", lambda: _args.command],
		["delay_multiplier", lambda: _args.delay_multiplier],
		["verbose", lambda: _args.verbose],
		["do_clean", lambda: _args.do_clean],
		["do_backup", lambda: _args.do_backup],
		["backup_location", lambda: _args.backup_location],
		["do_remove_all", lambda: _args.all],
	])

	if args.command == "review":
		print("Reviewing the log file is not yet implemented, exiting...")
		exit(1)

	if args.delay_multiplier < 0 or args.delay_multiplier == 0:
		print("Delay multiplier must be greater than 0, exiting...")
		exit(1)

	if args.do_backup and args.backup_location is None:
		print("Must specify backup location if backing up, exiting...")
		exit(1)

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
		backup_build_dir()
		clean_build_dir(args.verbose, args.do_remove_all)
	
	elif args.command == "backup":
		backup_build_dir()
	
	print_info("[ Done, enjoy your day coding :D ]")


if __name__ == "__main__":
 	main()