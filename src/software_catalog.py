#!/usr/bin/env python
"""
Provindexes a software catalog to store data about software.
"""

from pathlib import Path
import pickle
from software_program import SoftwareProgram


class SoftwareCatalog:
    """
    Stores data about software
    """
    def __init__(self, catalog_name):
        self.catalog_path = Path(catalog_name)
        if not self.catalog_path.is_file():
            print("The software catalog does not exist. Creatring...")
            catalog = open(self.catalog_path, "wb")
            pickle.dump([], catalog)
            print(str(self.catalog_path) + " created.")
            catalog.close()

    def __str__(self):
        return self.catalog_path

    def get_program(self, index: int) -> SoftwareProgram:
        """
        Returns a SoftwareProgram class
        """
        result = None
        file = open(self.catalog_path, "rb")
        for program in pickle.load(file):
            if program.index == index:
                result = program
        file.close()
        return result

    def add_program(self, program: SoftwareProgram):
        """
        Append to the list of software programs
        """
        file = open(self.catalog_path, "rb")
        program_list = pickle.load(file)
        program_list.append(program)
        file.close()
        file = open(self.catalog_path, "wb")
        pickle.dump(program_list, file)
        file.close()
