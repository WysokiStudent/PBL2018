#!/usr/bin/env python
"""
Provides a software catalog to store data about software.
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
            print("The software catalog does not exist. Creating...")
            catalog = open(self.catalog_path, "wb")
            tutorial = [SoftwareProgram(0, "Click me", "./", "./Tutorial.txt", "")]
            pickle.dump(tutorial, catalog)
            print(str(self.catalog_path) + " created.")
            catalog.close()

    def __str__(self):
        return self.catalog_path

    def __len__(self):
        catalog = open(self.catalog_path, "rb")
        length = len(pickle.load(catalog))
        catalog.close()
        return length

    def get_program(self, index: int) -> SoftwareProgram:
        """
        Returns a SoftwareProgram class
        """
        result = None
        catalog = open(self.catalog_path, "rb")
        for program in pickle.load(catalog):
            if program.index == index:
                result = program
        catalog.close()
        return result

    def update_program(self, program_to_update: SoftwareProgram):
        """
        Override entry in the program catalog
        """
        catalog = open(self.catalog_path, "r+b")
        program_list = pickle.load(catalog)

        for program in program_list:
            if program.index == program_to_update.index:
                program_list[program.index] = program_to_update
        catalog.seek(0)
        catalog.truncate()
        pickle.dump(program_list, catalog)
        catalog.close()

    def add_program(self, program: SoftwareProgram):
        """
        Append to the list of software programs
        """
        catalog = open(self.catalog_path, "rb")
        program_list = pickle.load(catalog)
        program_list.append(program)
        catalog.close()
        catalog = open(self.catalog_path, "wb")
        pickle.dump(program_list, catalog)
        catalog.close()

    def delete_program(self, program_index: int):
        """
        Delete from the list of software programs
        """
        catalog = open(self.catalog_path, "rb")
        program_list = pickle.load(catalog)
        catalog.close()
        for program in program_list:
            if program.index == program_index:
                program_list.remove(program)
        catalog = open(self.catalog_path, "wb")
        pickle.dump(program_list, catalog)
        catalog.close()

    def list_software(self) -> list:
        """
        Return list of programs stored inside catalog
        """
        catalog = open(self.catalog_path, "rb")
        result = pickle.load(catalog)
        catalog.close()

        return result
