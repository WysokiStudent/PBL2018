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

    def update_software_catalog(self, drive = None):
        """
        Using the software finder updates the repository that contains programs
        """
        import software_search
        if drive:
            print(drive)
            for software in software_search.get_software_list_from_file(drive):
                self.add_software(software)
        else:
            for software in software_search.get_software_list():
                self.add_software(software)
        # all_results_filename = "ScanResult.txt"
        # good_results_filename = "GoodScanResults.txt"
        # bruteSearch.scan_registry_and_save_results(
        #     all_results_filename,
        #     good_results_filename)


        # with open(all_results_filename, mode='r') as results:
        #     import ast
        #     for line in results:
        #         try:
        #             evaluated_line = ast.literal_eval(line)
        #             self.add_software(SoftwareProgram(str(evaluated_line[0]), str(evaluated_line[1]), "", ""))
        #         except Exception:
        #             self.add_software(SoftwareProgram(line, "", "", ""))


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

    def delete_software(self, program_index: int):
        self.catalog.delete_program(program_index)

    def list_installed_software(self) -> list:
        """
        Returns a list of SoftwarePrograms that are located in the repository
        """
        return self.catalog.list_software()
