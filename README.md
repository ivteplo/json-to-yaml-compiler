<h1 align="center">
    JSON to YAML compiler
</h1>

## Table of contents
- [Implementations](#implementations)
- [Development](#development)
    * [How to run tests](#how-to-run-tests)
    * [How to clean output files](#how-to-clean-output-files)
- [Important](#important)

## Implementations
__Currently avaliable implementations__:
- Python 3

Later on I'm going to write versions of compiler in other programming languages.

## Development
### How to run tests
To run tests, move to the folder of the implementation and run `make tests`. It will run script `test.py` from the `Scripts` folder in the project root with already specified needed environment variables. 

The another way is to run using bash:
```bash
cd [project-root-directory]
COMPILER_COMMAND="[command to run compiler]" ./Scripts/test.py
```

### How to clean output files
To clean all output files, open root folder of the project. Then run `make clean` or `./Scripts/clean.sh`. It will remove all folders `Implementations/[implementation-name]/TestResults`.

## Important
This project was created for studing writing compilers. So the implementations can be non-production-ready.

