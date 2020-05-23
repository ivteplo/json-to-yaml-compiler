#!/usr/bin/env python3
# 
# Copyright (c) 2020 Ivan Teplov
# Licensed under the Apache License, version 2.0
#

import os
import shutil
from pathlib import Path

implementations_path = Path(__file__).parent.parent / "Implementations"
implementations_folders = []

for (dirpath, dirnames, filenames) in os.walk(str(implementations_path)):
    implementations_folders = dirnames
    break

for folder in implementations_folders:
    test_path = implementations_path / folder / "TestResults"

    if os.path.isdir(str(test_path.resolve())):
        try:
            shutil.rmtree(str(test_path))
        except OSError as e:
            print("Error: {} : {}".format(str(test_path), e.strerror))
            continue
        print("Directory {} removed".format(str(test_path)))
    else:
        print("Folder {} not found. Continuing".format(str(test_path)))

print("Cleaning finished")

