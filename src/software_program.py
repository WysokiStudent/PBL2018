#!/usr/bin/env python

"""
Provindexes a structure to store information about software and it's license.
"""


class SoftwareProgram:
    """
    Structure to store information about software and it's license.
    """
    def __init__(
            self,
            name=None,
            program_location=None,
            license_location=None,
            note=None):
        self.index = None
        self.name = name
        self.program_location = program_location
        self.license_location = license_location
        self.license_location = license_location
        self.note = note

    def __str__(self):
        return str(self.name) + " " +\
            str(self.program_location) + " " +\
            str(self.license_location) + " " +\
            str(self.note)
