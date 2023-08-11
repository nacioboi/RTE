//
// file name: 			command-helper.c
//
// project:  			┌ RTE (Runtime Execute)
//					└── Command Helper
//
// version: 			0.0.1
//
// file description: 		N/A
//
// project description: 	an extremely simple library to compile and attach c code to the current process using gcc and the linux kernel.
//
// start date: 			03/04/2023
//
// credits:       		Joel Watson
// 







// the `popen` function will execute a given command and return a handle that connects to the pipe
//  of the existing command.
// NOTE: the popen function is a possible cancellation point, meaning that it can crash the program. 







#include "command-helper.h"







/// we are going to execute the command and redirect the stdout and stderr to different files.
int CommandHelper__runCommand ( char * input , void_ret__str_arg__func_ptr_t handle_stdout , void_ret__str_arg__func_ptr_t handle_stderr ) {



	// assign the out buffers
	char stdout_out [ COMMAND_HELPER__STDOUT_BUFFER_SIZE ];
	char stderr_out [ COMMAND_HELPER__STDERR_BUFFER_SIZE ];



	// define the file handles for stdout and stderr
	FILE * stdout_handle;
	FILE * stderr_handle;



	// generate the modified command in order to redirect stdout and stderr to different files
	// this is just temp, we will use something else later (like temp file library).
	char command [ 512 ];
	snprintf ( command , sizeof(command) , "%s 2>%s" , input , "/tmp/CommandHelper.stderr.123.xyz.log" );



	// see line 24
	stdout_handle = popen ( command , "r" );



	// get the stdout
	while ( 1 ) {

		char * out = fgets ( stdout_out , sizeof(stdout_out) , stdout_handle );

		if ( out == NULL ) { break; }

		// call the function pointer so that the users of this lib can handle the output as it gets generated.
		( *handle_stdout ) ( out );

	}



	// close the process handle
	pclose ( stdout_handle );



	// open a file handle for the redirected stderr
	stderr_handle = fopen ( "/tmp/CommandHelper.stderr.123.xyz.log" , "r" );



	// get the stderr
	while ( 1 ) {

		char * out = fgets ( stderr_out , sizeof(stderr_out) , stderr_handle );

		if ( out == NULL ) { break; }

		// call the function pointer so that the users of this lib can handle the output as it gets generated.
		( *handle_stderr ) ( out );

	}



	// close the stderr file handle.
	fclose ( stderr_handle );



	// done
	return 0;



}

