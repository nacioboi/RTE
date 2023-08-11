//
// file name: 			execution-helper.h
//
// project:  			┌ RTE (Runtime Execute)
//					└── Execution Helper
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



#include <spawn.h>



#define ___SYSTEM_EXECUTE___(program, ...) 															\
	pid_t ___SYSTEM_MACRO__PID___; 													\
	char * const ___SYSTEM_MACRO__ARGS___ [] = { program , __VA_ARGS__ , NULL }; 						\
	posix_spawn ( &___SYSTEM_MACRO__PID___ , program , NULL , NULL , ___SYSTEM_MACRO__ARGS___, NULL ); 		\
																			\
	int ___SYSTEM_MACRO__STATUS___; 													\
	waitpid ( ___SYSTEM_MACRO__PID___ , &___SYSTEM_MACRO__STATUS___ , 0 ); 							\
																			\
	int ___SYSTEM_MACRO__NEW_STATUS___;													\
																			\
	if ( WIFEXITED(___SYSTEM_MACRO__STATUS___) ) { 											\
		___SYSTEM_MACRO__NEW_STATUS___ = WEXITSTATUS(___SYSTEM_MACRO__STATUS___); 					\
	} else { 																	\
		___SYSTEM_MACRO__NEW_STATUS___ = -1; 											\
	}



#define SYSTEM_EXECUTE(argument) ___SYSTEM_EXECUTE___("/bin/bash", "-c", argument)



#define ___HIDE_POSTFIX___ "> /dev/null 2>&1"


#define SYSTEM_EXECUTE_HIDDEN(argument) ___SYSTEM_EXECUTE___("/bin/bash", "-c", argument, ___HIDE_POSTFIX___)


#define SYSTEM_GET_STATUS() ___SYSTEM_MACRO__NEW_STATUS___