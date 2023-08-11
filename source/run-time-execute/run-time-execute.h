//
// file name: 			run-time-execute.h
//
// project:  			RTE (Runtime Execute)
//
// version: 			0.0.1
//
// file description: 		N/A
//
// project description: 	an extremely simple library to compile and attach
// c code to the current process using gcc and the linux kernel.
//
// start date: 			03/04/2023
//
// credits:       		Joel Watson
//

#pragma once

#define bool char
#define true 1
#define false 0

// define some error codes
#define RUN_TIME_EXECUTE__ERROR__MALLOC_FAILED -1
#define RUN_TIME_EXECUTE__ERROR__READING_FILE_FAILED -2
#define RUN_TIME_EXECUTE__ERROR__WRITING_FILE_FAILED -3

#define RUN_TIME_EXECUTE__ERROR__FILE_TO_COPY_HANDLE_FAILED -4
#define RUN_TIME_EXECUTE__ERROR__BOTH_FILES_TO_COPY_HANDLES_FAILED -5
#define RUN_TIME_EXECUTE__ERROR__NEW_FILE_HANDLE_FAILED -6

#include <string.h>

#include "../command-helper/command-helper.h"
#include "../execution-helper/execution-helper.h"

typedef char *(*str_ret__str_arg__func_ptr_t)(char *);
typedef int (*int_ret__str_arg__func_ptr_t)(char *);

typedef int (*int_ret___str_ret__str_arg__func_ptr__arg___func_ptr_t)(int);

typedef struct {

	/// @note 						DO NOT SET DIRECTLY , THIS IS
	/// INTERNAL STATE
	/// .
	/// @brief 						the modified code returned by the
	/// function that was parsed
	///							in by pointer to the
	///`modifyBeforeExecution` function .
	char *modifiedCode;

	/// @note 						DO NOT SET DIRECTLY , THIS IS
	/// INTERNAL STATE
	/// .
	/// @brief 						a flag that is set to true when
	/// the `modifyBeforeExecution` function is done modifying the code .
	bool isDoneModifying;

	/// @note 						DO NOT SET DIRECTLY , THIS IS
	/// INTERNAL STATE
	/// .
	/// @brief 						a flag that is set to true when
	/// the `modifyBeforeExecution` function is called .
	/// both the `modifyBeforeExecution` and `executeFileAtRunTime` functions
	/// will
	/// check this flag . 							if any of these functions
	/// detect the flag is set to true , they will wait until the
	/// `isDoneModifying` flag is set to true , after which , they will read
	/// the `modifiedCode` instead of reading the file to execute.
	bool isModifyingBeforeExecuting;

	/// @brief 						call this function in order to modify
	/// the code to be executed before it is executed .
	/// @param handler 				a function pointer ( of which
	/// you have created ) to a function that takes a string and returns a
	/// string
	/// .
	///  							this function will take in the code to be
	///  executed and should return the modified code .
	/// 							when this function is called ,
	/// the `isModifyingBeforeExecuting` flag will be set to true .
	/// @return 					0 if successful , -1 if failed .
	int_ret___str_ret__str_arg__func_ptr__arg___func_ptr_t
		modifyBeforeExecution;

	/// @brief 						compiles and executes a file at
	/// run time
	/// .
	/// @param path_of_file_to_execute 		the FULL path of the file to
	/// execute .
	/// @return 					0 if successful , -1 if failed .
	int_ret__str_arg__func_ptr_t executeFileAtRunTime;

	/// @brief 						compiles and executes a file at
	/// run time
	/// .
	/// @param path_of_file_to_execute 		the FULL path of the file to
	/// execute .
	/// @return 					0 if successful , -1 if failed .
	int_ret__str_arg__func_ptr_t executeCodeAtRunTime;

} RunTimeExecute;

/// @brief initializes a new RunTimeExecute struct with all the function
/// pointers setup.
/// @return a new RunTimeExecute struct.
RunTimeExecute RunTimeExecute__init();

/// @note 						DO NOT CALL THIS FUNCTION DIRECTLY , INSTEAD
/// , CREATE A NEW `RunTimeExecute` STRUCT BY
///  							CALLING THE `RunTimeExecute__init`
///  FUNCTION
///  .
/// @brief 						call this function in order to modify the
/// code to be executed before it is executed .
/// @param handler 				a function pointer ( of which you have created
/// ) to a function that takes a string and returns a string .
///  							this function will take in the code to be executed
///  and should return the modified code .
/// 							when this function is called , the
/// `isModifyingBeforeExecuting` flag will be set to true .
/// @return 					0 if successful , -1 if failed .
int ___RunTimeExecute__modifyBeforeExecution___(
	str_ret__str_arg__func_ptr_t handler);

/// @note 						DO NOT CALL THIS FUNCTION DIRECTLY , INSTEAD
/// , CREATE A NEW `RunTimeExecute` STRUCT BY
///  							CALLING THE `RunTimeExecute__init`
///  FUNCTION
///  .
/// @brief 						compiles and executes a file at run
/// time
/// .
/// @param path_of_file_to_execute 		the FULL path of the file to execute .
/// @return 					0 if successful , -1 if failed .
int ___RunTimeExecute__executeFileAtRunTime___(char *path_of_file_to_execute);

/// @note 						DO NOT CALL THIS FUNCTION DIRECTLY , INSTEAD
/// , CREATE A NEW `RunTimeExecute` STRUCT BY
///  							CALLING THE `RunTimeExecute__init`
///  FUNCTION
///  .
/// @brief 						compiles and executes a file at run
/// time
/// .
/// @param path_of_file_to_execute 		the FULL path of the file to execute .
/// @return 					0 if successful , -1 if failed .
int ___RunTimeExecute__executeCodeAtRunTime___(char *path_of_file_to_execute);
