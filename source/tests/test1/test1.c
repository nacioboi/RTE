#include "../../run-time-execute/run-time-execute.h"

int main (void) {
	printf ( "hello from main func!\n" );
	// NOTE: must provide full path to file
	//___RunTimeExecute__executeFileAtRunTime___( "/Users/joel-watson/Documents/Programming Projects/C/RTE/source/tests/test1/run-time-target.c" );
	___RunTimeExecute__executeFileAtRunTime___( "/Users/joel-watson/Documents/Programming Projects/All/RTE/source/tests/test1/run-time-target.c" );
	printf ( "hello from main func pt2!\n" );
}