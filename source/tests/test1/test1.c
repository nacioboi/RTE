#include "../../run-time-execute/run-time-execute.h"

int main(void) {
	printf("hello from main func!\n");
	RunTimeExecute rte = RunTimeExecute__init();
	rte.executeFileAtRunTime(
		"/Users/joel-watson/Documents/Programming "
		"Projects/All/RTE/source/tests/test1/run-time-target.c");
	printf("hello from main func pt2!\n");
}