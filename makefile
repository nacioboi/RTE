input-dir 					="./source"
output-dir 					="./built"

command-helper-input 			="${input-dir}/command-helper/command-helper.c"
command-helper-output 			="${output-dir}/command-helper/command-helper.o"

run-time-execute-input 			="${input-dir}/run-time-execute/run-time-execute.c"
run-time-execute-intermediate 	="${output-dir}/run-time-execute/run-time-execute.o"
run-time-execute-output 		="${output-dir}/run-time-execute/librun-time-execute.a"

test1-input 				="${input-dir}/tests/test1/test1.c"
test1-intermediate 			="${output-dir}/tests/test1/test1.o"
test1-output 				="${output-dir}/tests/test1/test1"



tests: rte
	gcc -c ${test1-input} -o ${test1-intermediate}
	gcc ${test1-intermediate} -o ${test1-output} -L"./built/run-time-execute" -lrun-time-execute



ch:
	gcc -c ${command-helper-input} -o ${command-helper-output}



rte: ch
	gcc -c ${run-time-execute-input} -o ${run-time-execute-intermediate}
	ar rcs ${run-time-execute-output} ${run-time-execute-intermediate} ${command-helper-output}


clean:
	rm ./built/command-helper/*
	rm ./built/run-time-execute/*
	rm ./built/tests/test1/*