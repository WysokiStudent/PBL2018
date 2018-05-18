#!/usr/bin/env python

from software_program import *
from software_license_organiser import *
import appJar

APP = appJar.gui("Software Organiser", useTtk=True)
CATALOG = SoftwareLicenseOrganiser("softwares.pi")

def create_software_list(software_list, row: int, column: int):
    APP.startFrame("Software List Frame", row, column)
    APP.setSticky("nsew")
    APP.addListBox("Software List", software_list).bind("<Double-Button-1>", edit_list_entry, add="+")
    APP.setListBoxChangeFunction("Software List", change_license_text);
    APP.stopFrame()

def create_license_box(row: int, column: int):
    APP.startLabelFrame("License", row, column)
    APP.setSticky("nsew")
    APP.addTextArea("License Text", row + 1, column)
    APP.setTextArea("License Text", """To view the licese of a software click on the software list entry on the left.""")
    APP.stopLabelFrame()

def create_edit_window():
    APP.startSubWindow("Edit List Entry", "Edit")
    APP.setSticky("nsew")
    APP.addLabel("Program Index Label", "Index")
    APP.addLabelEntry("Name Entry")
    APP.addLabelFileEntry("Program Location Entry")
    APP.addLabelFileEntry("License Location Entry")
    APP.addLabelEntry("Notes Entry")
    APP.addButton("Submit changes", submit_list_entry_change)
    APP.stopSubWindow()

def change_license_text(list_changed_event):
    software = APP.getListBox("Software List")[0]
    APP.clearTextArea("License Text")
    license_location = CATALOG.get_software(int(software.split()[0])).license_location
    try:
        with open(license_location, "r") as file:
            text = file.read().replace("\n", "")
        APP.setTextArea("License Text", text)
    except:
        print("Could not open " + license_location)
        APP.setTextArea("License Text", "Failed to open file.")

def submit_list_entry_change(event):
    software_index = int(APP.getLabel("Program Index Label").split()[-1])
    software = CATALOG.get_software(software_index)
    software.name = APP.getEntry("Name Entry")
    software.program_location = APP.getEntry("Program Location Entry")
    software.license_location = APP.getEntry("License Location Entry")
    software.note = APP.getEntry("Notes Entry")

    CATALOG.update_software(software)
    APP.updateListBox("Software List", CATALOG.list_installed_software(), callFunction=False)

def edit_list_entry(event):
    index = APP.getListBox("Software List")[0].split()[0]
    software = CATALOG.get_software(int(index))
    APP.setLabel("Program Index Label", "Program Index: " + index)
    APP.setEntry("Name Entry", software.name)
    APP.setEntry("Program Location Entry", software.program_location)
    APP.setEntry("License Location Entry", software.license_location)
    APP.setEntry("Notes Entry", software.note)
    APP.showSubWindow("Edit List Entry")

def main():
    create_software_list(CATALOG.list_installed_software(), 0, 0)
    create_license_box(0, 1)
    create_edit_window()
    APP.addMenu("menu", None)
    APP.go()

if __name__ == "__main__":
    main()
