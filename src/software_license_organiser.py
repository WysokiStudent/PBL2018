#!/usr/bin/env python
"""
The software license organiser works a bridge between the GUI, the data storage
and the software finder
"""


from software_program import SoftwareProgram
from software_catalog import SoftwareCatalog


class SoftwareLicenseOrganiser:
    """
    SoftwareLicenseOrganiser is used to simplyfy communication inside
    the program
    """
    def __init__(self, catalog_location):
        self.catalog = SoftwareCatalog(catalog_location)
        self.lister = None

    def update_software_catalog(self):
        """
        Using the software finder updates the repository that contains programs
        """
        print("Currently unavailable")

    def get_software(self, index: int) -> SoftwareProgram:
        """
        Returns the SoftwareProgram with the index given as the parameter.
        """
        return self.catalog.get_program(index)

    def update_software(self, program: SoftwareProgram):
        """
        Overrites a single entry inside the catalog.
        """
        self.catalog.update_program(program)


    def add_software(self, program: SoftwareProgram):
        """
        Adds program to repository
        """
        index = len(self.catalog)
        program.index = index
        self.catalog.add_program(program)

    def list_installed_software(self) -> list:
        """
        Returns a list of SoftwarePrograms that are located in the repository
        """
        return self.catalog.list_software()
