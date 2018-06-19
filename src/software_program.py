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
            name=None,
            program_location=None,
            license_location=None,
            note=None):
        self.index = index
        self.name = name
        self.program_location = program_location
        self.license_location = license_location
        self.note = note

    def __str__(self):
        return ''.join([
            str(self.index), ' ', str(self.name), ' ',
            str(self.program_location), ' ',
            str(self.license_location), ' ',
            str(self.note)])
