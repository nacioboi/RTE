# This Makefile uses the following automatic variables:
# $@ : The file name of the target of the rule.
# $< : The name of the first prerequisite.
# $^ : The names of all the prerequisites.

# Relative is so that any untracked build files are absolutely deleted when running clean.
base-dir = ./built
input-dir = ../source  # relative to $(base-dir).
output-dir = .  # relative to $(base-dir).

command-helper-input = $(input-dir)/command-helper/command-helper.c
command-helper-output = $(output-dir)/command-helper/command-helper.o

run-time-execute-input = $(input-dir)/run-time-execute/run-time-execute.c
run-time-execute-intermediate = $(output-dir)/run-time-execute/run-time-execute.o
run-time-execute-output = $(output-dir)/run-time-execute/librun-time-execute.a

test1-input = $(input-dir)/tests/test1/test1.c
test1-intermediate = $(output-dir)/tests/test1/test1.o
test1-output = $(output-dir)/tests/test1/test1

gcc-args = -Wall -Wextra -Wshadow -Wconversion -Wuninitialized -Wunused -Wstrict-prototypes -Wcast-align -Wlogical-op -Wformat-security -Wdangling-else -Wdouble-promotion -Wformat=2 -march=native -O3
compiler = gcc $(gcc-args)

all: tests

$(command-helper-output): $(command-helper-input)
	$(compiler) -c $< -o $@

$(run-time-execute-intermediate): $(run-time-execute-input)
	$(compiler) -c $< -o $@

$(run-time-execute-output): $(run-time-execute-intermediate) $(command-helper-output)
	ar rcs $@ $^

$(test1-intermediate): $(test1-input)
	$(compiler) -c $< -o $@

$(test1-output): $(test1-intermediate)
	$(compiler) $< -o $@ -L$(output-dir)/run-time-execute -lrun-time-execute

tests: $(test1-output)

backup:
	tar -czvf $(base-dir)/../../backup.tar.gz $(base-dir)/..

clean: backup
	rm -rf $(output-dir)
