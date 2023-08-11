//
// file name: 			command-helper.h
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



#pragma once



#ifndef COMMAND_HELPER__STDOUT_BUFFER_SIZE

#define COMMAND_HELPER__STDOUT_BUFFER_SIZE 512

#endif



#ifndef COMMAND_HELPER__STDERR_BUFFER_SIZE

#define COMMAND_HELPER__STDERR_BUFFER_SIZE 512

#endif



#include <stdio.h>
#include <stdlib.h>



typedef void ( * void_ret__str_arg__func_ptr_t ) ( char * );



int CommandHelper__runCommand ( char * input , void_ret__str_arg__func_ptr_t handle_stdout , void_ret__str_arg__func_ptr_t handle_stderr );