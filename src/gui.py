#!/usr/bin/env python

from software_program import *
import appJar

APP = appJar.gui("Software Organiser")
SOFTWARE_LIST = [SoftwareProgram(), SoftwareProgram("Microsoft", "D:", "F:"), SoftwareProgram("Intelij", "C:/S")]

def create_software_list(software_list, row: int, column: int):
    APP.startFrame("Software List Frame", row, column)
    APP.setSticky("nsew")
    APP.addListBox("Software List", software_list)
    APP.setListBoxChangeFunction("Software List", change_license_text);
    APP.stopFrame()

def create_license_box(row: int, column: int):
    APP.startLabelFrame("License", row, column)
    APP.setSticky("nsew")
    APP.addTextArea("License Text", row + 1,column)
    APP.setTextArea("License Text", """This is where the string containing the actual license should be placed, hopefully it won't crash""")
    APP.stopLabelFrame()

def change_license_text(list_changed_event):
    program = APP.getListBox("Software List")[0]
    APP.clearTextArea("License Text")
    license_location = program.split()[2]
    APP.setTextArea("License Text", license_location)

def main():
    create_software_list(SOFTWARE_LIST, 0, 0)
    create_license_box(0, 1)
    APP.go()

if __name__ == "__main__":
    main()
