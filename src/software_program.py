#!/usr/bin/env python

"""
Provindexes a structure to store information about software and it's license.
"""

import os.path


class SoftwareProgram:
    """
    Structure to store information about software and it's license.
    """
    def __init__(
            self,
            index,
            name="",
            program_location="",
            license_location="",
            note=""):
        self.index = index
        self.name = name
        self.program_location = program_location
        self.license_location = license_location
        self.note = note

    def __str__(self):
        return "".join([
            str(self.index), " ", str(self.name).replace('.exe', ''), " ",
            str(self.program_location), " ",
            str(self.license_location), " ",
            str(self.note)])
