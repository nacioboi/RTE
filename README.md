# RTE ( Run Time Execute )

This project is a simple library for executing c code at run time .

<br/><br/>

## Use Cases :
- adding functionality on top of the c language by parsing the , *file to execute* .  the parsing / converting into correct c code is done by you .  this can be done with the , `RunTimeExecute__modifyBeforeExecute` function .
- downloading code from the web , or other source , and running it with ease . **SECURITY WARNING** BE CAREFUL WHAT CODE YOU RUN .

<br/>

> you may be asking , why run code from the web if it is a security risk ?  <br/><br/>
> one reason is if someone wants most of their code to be open source but they have some super secret , super saucy or otherwise , super fast algorithm that they need to keep secret from their competitors .  <br/><br/>
> to achieve this then , this hypothetical someone could give an opt-in option to the user asking if they would like to use their super secret code ( looking at you canonical ) and if the user accepts this option , this library could then be used as a way to run the code once it has been downloaded from this hypothetical someones server and written into the user's RAM .

<br/><br/>

## Project Structure :
- `./built` is a directory containing all the object files for the project .
- `./source` is a juicy directory containing all the source code .
	- `./source/command-helper` is a directory containing the sub-project , Command Helper . this sub-project then , allows the programmer to easily run a system command and get the stdout and stderr separately .
	- `./source/execution-helper` is a directory containing a simple header file that then contains a macro for running system commands , in a more crude way though , using the `spawn.h` header .
	- `./source/run-time-execute` is another directory containing the most succulent part of the project . it exposes only three  functions to the public , `RunTimeExecute__executeFileAtRunTime` , `RunTimeExecute__executeCodeAtRunTime` and , `RunTimeExecute__modifyBeforeExecute` .
	- `./source/tests` is a directory containing various tests that show simply how to use this library.

<br/><br/>

## How To Use :
- In order to use this library you will need:
	- a computer running a unix/like environment like macos or linux . if you're running windows , then you can use [WSL](https://learn.microsoft.com/en-us/windows/wsl/) ( Windows Sub-system for Linux ) .
	- a main file , from which your compilation target ( see below ) will be ran from . inside this file , you have two choices :
		- treat as an entire c file using `RunTimeExecute__executeFileAtRuntime`.
		- treat as part of the entire c file using `RunTimeExecute__executeCodeAtRunTime`. (see below for examples).
		- you may also choose to modify the code before executing by using `RunTimeExecute__modifyBeforeExecute` function.
