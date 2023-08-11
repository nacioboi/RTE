//
// file name: 			run-time-execute.c
//
// project: 			RTE (Runtime Execute)
//
// version: 			0.0.1
//
// file description: 		N/A
//
// project description: 	an extremely simple library to compile and
// attach c code to the current process using gcc and the linux kernel.
//
// start date: 			03/04/2023
//
// credits: 			Joel Watson
//

// this needs to be the exact location of this, the very file you are reading!
#define RUN_TIME_EXECUTE__SELF                                                 \
	"/Users/joel-watson/Documents/Programming "                              \
	"Projects/All/RTE/source/run-time-execute/run-time-execute.c"

#include "run-time-execute.h"

size_t ___RunTimeExecute__getFileSize___(FILE *file_handle) {
	long ret;

	fseek(file_handle, 0, SEEK_END);
	ret = ftell(file_handle);
	rewind(file_handle);

	return ret;
}

char *___RunTimeExecute__readFile___(char *path_of_file_to_read) {
	FILE *file_handle = fopen(path_of_file_to_read, "r");

	if (file_handle == NULL) {
		fclose(file_handle);

		return (char *)RUN_TIME_EXECUTE__ERROR__FILE_TO_COPY_HANDLE_FAILED;
	}

	size_t file_read_size = ___RunTimeExecute__getFileSize___(file_handle);

	char *file_read_buffer = (char *)malloc(file_read_size + 1);

	if (file_read_buffer == NULL) {
		perror("malloc failed to assign memory to the buffer.");

		fclose(file_handle);
		free(file_read_buffer);

		return (char *)RUN_TIME_EXECUTE__ERROR__MALLOC_FAILED;
	}

	size_t bytes_read =
		fread(file_read_buffer, 1, file_read_size, file_handle);

	if (bytes_read != file_read_size) {
		perror("reading from file failed.");

		fclose(file_handle);
		free(file_read_buffer);

		return (char *)RUN_TIME_EXECUTE__ERROR__READING_FILE_FAILED;
	}

	file_read_buffer[file_read_size] = '\0';

	return file_read_buffer;
}

int ___RunTimeExecute__duplicateFile___(char *path_of_file_to_duplicate,
						    char *new_file_name) {
	FILE *file_to_copy_handle;
	FILE *new_file_handle;

	file_to_copy_handle = fopen(path_of_file_to_duplicate, "r");
	new_file_handle = fopen(new_file_name, "w");

	if (file_to_copy_handle == NULL || new_file_handle == NULL) {
		// 0: `file_to_copy_handle` failed.
		// 1: `new_file_handle` failed.
		// 2: both failed.
		unsigned short type = 4;

		char message[128];

		if (file_to_copy_handle == NULL) {
			strcat(message, "`file_to_copy_handle`");
			type = 0;
		} else if (new_file_handle == NULL && type == 0) {
			strcat(message, " and `new_file_handle`");
			type = 2;
		} else {
			strcat(message, "`new_file_handle`");
			type = 1;
		}

		fclose(file_to_copy_handle);
		fclose(new_file_handle);

		strcat(message, " failed to initialize.\n");
		perror(message);

		if (type == 0) {
			return RUN_TIME_EXECUTE__ERROR__FILE_TO_COPY_HANDLE_FAILED;
		} else if (type == 2) {
			return RUN_TIME_EXECUTE__ERROR__BOTH_FILES_TO_COPY_HANDLES_FAILED;
		} else {
			return RUN_TIME_EXECUTE__ERROR__NEW_FILE_HANDLE_FAILED;
		}
	}

	size_t file_read_size =
		___RunTimeExecute__getFileSize___(file_to_copy_handle);

	char *file_read_buffer = malloc(file_read_size + 1);

	if (file_read_buffer == NULL) {
		perror("malloc failed to assign memory to the buffer.");

		fclose(file_to_copy_handle);
		fclose(new_file_handle);

		free(file_read_buffer);

		return RUN_TIME_EXECUTE__ERROR__MALLOC_FAILED;
	}

	size_t bytes_read =
		fread(file_read_buffer, 1, file_read_size, file_to_copy_handle);

	if (bytes_read != file_read_size) {
		perror("reading from file failed.");

		fclose(file_to_copy_handle);
		fclose(new_file_handle);

		return RUN_TIME_EXECUTE__ERROR__MALLOC_FAILED;
	}

	file_read_buffer[file_read_size] = '\0';

	size_t bytes_written = fwrite(file_read_buffer, 1,
						strlen(file_read_buffer), new_file_handle);

	if (bytes_written != strlen(file_read_buffer)) {
		perror("writing to file failed.");

		fclose(file_to_copy_handle);
		fclose(new_file_handle);

		return RUN_TIME_EXECUTE__ERROR__WRITING_FILE_FAILED;
	}

	fclose(file_to_copy_handle);
	fclose(new_file_handle);

	free(file_read_buffer);

	return 0;
}

int ___RunTimeExecute__compileFile___(char *path_of_file_to_compile) {
	___RunTimeExecute__duplicateFile___(path_of_file_to_compile,
							"__temp_comp_targ__.c");

	SYSTEM_EXECUTE(
		"gcc -g -Wall -O3 __temp_comp_targ__.c -o __a__.out"); //,"-g","-Wall","-O3","%s");

	return 0;
}

void ___RunTimeExecute__handleStandardOutput___(char *line_of_stdout) {
	printf("%s\n", line_of_stdout);
}

void ___RunTimeExecute__handleStandardError___(char *line_of_stderr) {
	printf("%s\n", line_of_stderr);
}

int ___RunTimeExecute__executeFile___(char *path_of_file_to_execute) {
	void (*handle_stdout_ptr)(char *) =
		___RunTimeExecute__handleStandardOutput___;
	void (*handle_stderr_ptr)(char *) =
		___RunTimeExecute__handleStandardError___;

	return CommandHelper__runCommand("./__a__.out", handle_stdout_ptr,
						   handle_stderr_ptr);
}

int ___RunTimeExecute__executeFileAtRunTime___(char *path_of_file_to_execute) {
	int ret = 0;

	___RunTimeExecute__compileFile___(path_of_file_to_execute);
	ret = ___RunTimeExecute__executeFile___(path_of_file_to_execute);

	return ret;
}

RunTimeExecute RunTimeExecute__init() {
	RunTimeExecute s;
	s.executeFileAtRunTime = &___RunTimeExecute__executeFileAtRunTime___;
	// s.executeCodeAtRunTime = ___RunTimeExecute__executeCodeAtRunTime___;
	return s;
}