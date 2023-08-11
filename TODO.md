# TODO List for Runtime Execute (RTE)

### Sorted from highest to lowest priority.

## Functionality
- [ ] Outline a strategy for concurrent Just-In-Time compilation and execution of split C code blocks at runtime.
- [ ] Begin implementation for the `executeCodeAtRunTime` function. It should compile and execute actual C code passed as a string at runtime. For now this means just adding a main function to the code string and compiling it.

## Testing
- [ ] Write more tests to cover more use cases.
- [ ] Begin an implementation for a formal Unit Testing suite to ensure the functionality of individual parts.

## Documentation
- [ ] Improve function/api comments so that devs working with the library can understand the code directly within their editor.
- [ ] Begin to write a suite of documentations in a `docs` folder to help users understand how to use the library.

## Security
- [ ] Improve security associated with the use of temporary files. Currently, paths and names for these files are hard-coded which could cause potential file conflicts or security vulnerabilities.
- [ ] Evaluate potential security risks associated with running commands directly in the shell.

## Concurrency
- [ ] Add built-in support for handling concurrency or parallel execution.

## Compatibility
- [ ] Enhance cross-platform compatibility. Currently, the library is highly specific to the Linux operating system and the GCC compiler. It would be beneficial to support other platforms and compilers.
