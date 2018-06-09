#!/usr/bin/env python
"""
The software license organiser works a bridge between the GUI, the data storage
and the software finder
"""


from software_program import SoftwareProgram
from software_catalog import SoftwareCatalog
import bruteSearch


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
        all_results_filename = "ScanResult.txt"
        good_results_filename = "GoodScanResults.txt"
        bruteSearch.scan_registry_and_save_results(
            all_results_filename,
            good_results_filename)

        with open(all_results_filename, encoding='latin-1', mode='r') as results:
            for line in results:
                self.add_software(SoftwareProgram(line, "", "", ""))


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
