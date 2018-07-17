#!/usr/bin/env python3

import os
import stat

enabled = True
description = "Create and empty file and assigned permissions."


def check_level(user):
    """
    Level 1

    Goal(s):

        * Create a folder "L0001" in your `~/game/` folder
        * Create an empty file in `~/game/L0001/` named "test.txt"
        * Assign that file the following permissions:
            * User: Read, Write, Execute
            * Group: None
            * Other: None
    """
    success = False

    filepath = os.path.join("/", "home", user, "game", "L0001", "test.txt")

    if os.path.isfile(filepath):
        stats = os.stat(filepath)
        permissions = stat.filemode(stats.st_mode)
        if permissions == "-rwx------" and os.path.getsize(filepath) == 0:
            success = True

    return success
