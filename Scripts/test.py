#!/usr/bin/env python3
# 
# Copyright (c) 2020 Ivan Teplov
# Licensed under the Apache License, version 2.0
#
import os
import sys
import platform
import subprocess
from pathlib import Path

compiler_env_var_name = "COMPILER_COMMAND"

if not compiler_env_var_name in os.environ:
    print("Compiler is not specified")
    quit()

files = []
compiler_command = os.environ[compiler_env_var_name]
tests_path = Path(__file__).parent.parent.resolve() / "Tests/"
output_path = Path(os.getcwd()) / "TestResults"

try:
    output_path.mkdir(parents=True, exist_ok=True)
except OSError:
    print("Could not create directory {}".format(str(output_path)))
    quit(1)
else:
    print("Created directory {}".format(str(output_path)))

def read_file(file):
    for i in file:
        yield i

for (dirpath, dirnames, filenames) in os.walk(str(tests_path)):
    files = filenames
    break

for file in files:
    if file[-5:len(file)] != ".json":
        continue

    print("---")
    print(file + ":")

    shell = True
    output_file = output_path / (file + ".yaml")
    expected_result_file = tests_path / (file[0:-4] + "yaml")
    command = compiler_command.split(" ")
    command.extend([
        str(tests_path / file),
        "--output",
        str(output_file)
    ])

    if platform.system() == "Linux":
        shell = False

    result = subprocess.run(command, shell = shell, cwd=os.getcwd())

    if result.returncode != 0:
        print("Error while running compiler")
        continue
    
    with open(str(expected_result_file), "r") as file_expect, open(str(output_file), "r") as file_result:
        read_exp = read_file(file_expect)
        read_res = read_file(file_result)

        while True:
            line_exp = next(read_exp, None)
            line_res = next(read_res, None)

            if line_exp == None or line_res == None:
                if line_exp == line_res:
                    # passed
                    print("Test passed")
                    break
                else:
                    print("Test is not passed")
                    break
            elif line_exp != line_res:
                print("Test is not passed")
                break

print("---")

