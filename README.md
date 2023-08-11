# Runtime Execute (RTE)

## :warning: Disclaimer :warning:

This project is currently a **Work In Progress** and is in its early development stage. Some features may not be fully implemented yet, and the library has not undergone comprehensive testing and debugging.

Significant portions of the current code are subject to change.

Specifically, the following functionalities are not implemented yet:

* The `executeCodeAtRunTime` function is not currently operational. When complete, this function will compile and execute actual C code passed as a string at runtime.

* The `modifyBeforeExecution` function is meant to allow modifications of code before execution. However, it is not fully functional in the current version.

* The code is highly specific to the Linux operating system and the GCC compiler. Cross-platform compatibility and support for multiple compilers are areas for future improvement.

> Note: Don't be confused by the functions `executeFileAtRunTime` and `executeCodeAtRunTime`. The former is operational and allows you to run an external C file at runtime. The latter is not yet operational and will allow you to run actual C code passed as a string at runtime. For now, I'll leave the names of these functions as they are, but I may change them in the future to avoid confusion.

Please exercise caution when integrating this library into your projects. Your constructive feedback and contributions can help me to refine this tool and develop it further.

## Introduction

Runtime Execute (RTE) aims to be a simple, lightweight C library that lets you compile, attach, and execute C code at runtime using GCC and the Linux kernel.

I'm developing this because I firmly believe there's no limit to what C code can do; if anyone says C code cannot be executed at runtime, I confidently challenge that idea. :smiling_imp:

## Use cases:

* **Opt-In Code Execution**: Imagine a mostly open-source company with a revolutionary or ultra-fast algorithm they want to keep from competitors - they can present an opt-in option to users, within their open source code, asking to run their proprietary code. Once the user accepts, this library could execute the downloaded code. This would allow the company to keep their code secret while still providing the benefits of open source. :D

## Features

* **Run C Files at Runtime**: You can use the library's `executeFileAtRunTime` function to compile and run an external C file at runtime.

* **Run Code Strings at Runtime**: The planned `executeCodeAtRunTime` function will compile and execute actual C code passed as a string at runtime.

* **Code Modification**: Use the `modifyBeforeExecution` function to customize code before it's compiled and executed. The argument is a function pointer: this function should accept a string of code and return the modified code string.

## Requirements

1. GCC (GNU Compiler Collection)
2. Linux kernel
3. A POSIX compliant shell (bash, etc.)

## Installation

Integration of the library into your existing C project is straightforward and requires no dependencies outside of the standard C library.

## Usage

Please refer to the included tests to understand usage in more detail.

**Test1:**

This test demonstrates how to initialize the RunTimeExecute module and run an external C file. 

```c
#include "../../run-time-execute/run-time-execute.h"

int main(void) {
  printf("hello from main func!\n");
  RunTimeExecute rte = RunTimeExecute__init();
  rte.executeFileAtRunTime(
    "/Users/joel-watson/Documents/Programming "
    "Projects/All/RTE/source/tests/test1/run-time-target.c");
  printf("hello from main func pt2!\n");
}
```
Ensure to change the path to match the location of your source file.

## Limitations

* This library is specifically made for a Linux environment using GCC. Using a different compiler or operating system may require significant modifications to the `execution-helper` and `run-time-execute` modules.

* Temporary files used during the compilation process have hardcoded names and locations, potentially leading to file conflicts or overly broad permissions. 

* The RTE library runs commands directly in the shell, so application security will depend on the security of your runtime environment and the security practices implemented during coding and testing.

* The RTE library doesn't provide a built-in mechanism for dealing with concurrency or parallel execution. If you need to run multiple pieces of code simultaneously, you'll need to manage that on your own.

## Contributions

I welcome any contributions and suggestions for improvement. Feel free to open an issue or submit a pull request.

## License

RTE is distributed under the GPL (GNU General Public License) 2.0. Please refer to `LICENSE` for more details.

#### Acknowledgements
A special shoutout to my AI assistant! :robot:
He's been a great help in developing this library and 90% of this readme. :smile:

