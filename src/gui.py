#!/usr/bin/env python

"""
The GUI for the software organiser.
"""

import appJar
from software_program import SoftwareProgram
from software_license_organiser import SoftwareLicenseOrganiser

APP = appJar.gui("Software Organiser", useTtk=True)
CATALOG = SoftwareLicenseOrganiser("softwares.pi")

def create_software_list(software_list, row: int, column: int):
    """
    Creates a Frame with a ListBox in wich the list of softwares is shown.
    """
    APP.startFrame("Software List Frame", row, column)
    APP.setSticky("nsew")
    APP.addListBox("Software List", software_list).bind(
        "<Double-Button-1>",
        edit_list_entry, add="+")
    APP.setListBoxChangeFunction("Software List", change_license_text)
    APP.stopFrame()

def create_license_box(row: int, column: int):
    """
    Creates a Frame in which an editable text box is placed, inside the textbox
    the license text is placed. Changing the text in the box will not change the contents
    of the file with the license. It will however change the text that will be sent to
    the license parser.
    """
    APP.startLabelFrame("License", row, column)
    APP.setSticky("nsew")
    APP.addTextArea("License Text", row + 1, column)
    APP.setTextArea(
        "License Text",
        """To view the licese of a software click on the software list entry on the left.""")
    APP.stopLabelFrame()

def create_edit_window():
    """
    Creates a window inside which the user can edit the contents of a selected list entry.
    The window is hidden by default.
    """
    APP.startSubWindow("Edit List Entry", "Edit", True)
    APP.setStretch("column")
    APP.setSticky("nsew")
    APP.addLabel("Program Index Label", "Index")
    APP.addLabelEntry("Name Entry")
    APP.addLabelFileEntry("Program Location Entry")
    APP.addLabelFileEntry("License Location Entry")
    APP.addLabelEntry("Notes Entry")
    APP.addButton("Submit changes", submit_list_entry_change)
    APP.stopSubWindow()

def change_license_text(list_changed_event):
    """
    Updates the textBox that stores the license to show the license of the currently selected
    list entry.
    """
    try:
        software = APP.getListBox("Software List")[0]
    except IndexError:
        return
    APP.clearTextArea("License Text")
    license_location = CATALOG.get_software(int(software.split()[0])).license_location
    try:
        with open(license_location, "r") as file:
            text = file.read().replace("\n", "")
        APP.setTextArea("License Text", text)
    except FileNotFoundError:
        print("Could not open " + license_location)
        APP.setTextArea("License Text", "Failed to open file.")

def submit_list_entry_change(event):
    """
    Accept changes to the list entry made by the user. The changes to be made are taken from
    the subwindow in which the user can make changes.
    """
    software_index = int(APP.getLabel("Program Index Label").split()[-1])
    software = CATALOG.get_software(software_index)
    software.name = APP.getEntry("Name Entry")
    software.program_location = APP.getEntry("Program Location Entry")
    software.license_location = APP.getEntry("License Location Entry")
    software.note = APP.getEntry("Notes Entry")

    CATALOG.update_software(software)
    APP.updateListBox("Software List", CATALOG.list_installed_software(), callFunction=False)
    APP.hideSubWindow("Edit List Entry")

def edit_list_entry(event):
    """
    Change the subwindow in whch the user can edit list entries to reflect the current contetns
    of the list entry that is selected.
    """
    index = APP.getListBox("Software List")[0].split()[0]
    software = CATALOG.get_software(int(index))
    APP.setLabel("Program Index Label", "Program Index: " + index)
    APP.setEntry("Name Entry", software.name)
    APP.setEntry("Program Location Entry", software.program_location)
    APP.setEntry("License Location Entry", software.license_location)
    APP.setEntry("Notes Entry", software.note)
    APP.showSubWindow("Edit List Entry")

def add_list_entry():
    """
    Adds an empty Program to the software catalog and then updates the list to reflect the change
    """
    CATALOG.add_software(SoftwareProgram("New Entry", "", "", ""))
    APP.updateListBox(
        "Software List",
        CATALOG.list_installed_software(),
        select=True,
        callFunction=True)
    edit_list_entry(None)

def parse_license():
    """
    Parse the text of the license that is currently stored inside the TextBox that displayes the
    license.
    """
    print("Currently unavaiable")

def scan_for_software():
    """
    Use an tool that scans the computer in search for installed software.
    """
    CATALOG.update_software_catalog()
    APP.updateListBox("Software List", CATALOG.list_installed_software())

def main():
    """
    Run the GUI for the software organiser
    """
    create_software_list(CATALOG.list_installed_software(), 0, 0)
    create_license_box(0, 1)
    create_edit_window()
    APP.setStretch("column")
    APP.addButton("Add Software", add_list_entry, 1, 0)
    APP.addButton("Parse License", parse_license, 1, 1)
    APP.addMenuList("Menu", ["Scan for Software"], [scan_for_software])
    APP.go()

if __name__ == "__main__":
    main()
