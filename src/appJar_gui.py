#!/usr/bin/env python

"""
The GUI for the software organiser.
"""

import _thread
import appJar
from software_program import SoftwareProgram
from software_license_organiser import SoftwareLicenseOrganiser
from license_web_analyzer import LicenseWebAnalyzer

APP = appJar.gui("Software Organiser", "800x500", useTtk=True)
CATALOG = SoftwareLicenseOrganiser("softwares.pi")
ANALIZER = LicenseWebAnalyzer()
scanning_in_progress = False
hide_files_not_containing_paths = False
hide_files_not_containing_licenses = False
license_directory = ""
software_search_value = ""
license_search_value = ""

def create_software_list(software_list, row: int, column: int, colspan=0, rowspan=0):
    """
    Creates a Frame with a ListBox in which the list of softwares is shown.
    """
    APP.startFrame("Software List Frame", row, column, colspan, rowspan)
    APP.setSticky("nsew")
    APP.addListBox("Software List", software_list).bind(
        "<Double-Button-1>",
        edit_list_entry, add="+")
    APP.setListBoxChangeFunction("Software List", update_license_list)
    APP.stopFrame()

def create_license_list(row: int, column: int, colspan=0, rowspan=0):
    """
    Creates a Frame with a ListBox in which the list of licenses is shown.
    """
    APP.startFrame("License List Frame", row, column, colspan, rowspan)
    APP.setSticky("nsew")
    APP.addListBox("License List", get_license_list())
    APP.setListBoxChangeFunction("License List", change_license_text)
    APP.stopFrame()

def get_license_list():
    """
    Gets a list of files from path "license_location"
    """
    global license_directory
    files = []
    try:
        index = get_software_index()
    except IndexError:
        return files
    software = CATALOG.get_software(index)
    
    if software.license_location != "":
        import os, glob
        if os.path.isdir(software.license_location):
            license_directory = software.license_location
            files.extend(os.path.basename(file) for file in glob.iglob("".join([software.license_location, "/*"])))
        elif os.path.isfile(software.license_location):
            license_directory, file = os.path.split(software.license_location)
            files.append(file)
        for index, file in enumerate(files.copy()):
            if license_search_value.casefold() not in file.casefold():
                del files[index]
    return files

def create_license_box(row: int, column: int, colspan=0, rowspan=0):
    """
    Creates a Frame in which an editable text box is placed.
    Inside the textbox the license text is placed.
    Changing the text in the box will not change the contents of the file
    with the license. It will however change the text that will be sent to
    the license parser.
    """
    APP.startLabelFrame("License", row, column, colspan, rowspan)
    APP.setSticky("nsew")
    APP.addTextArea("License Text", row + 1, column)
    APP.setTextArea(
        "License Text",
        "To view the license of a software click on the software entry" +
        " on the left.")
    APP.stopLabelFrame()

def create_edit_window():
    """
    Creates a window inside which the user can edit
    the contents of a selected list entry.
    The window is hidden by default.
    """
    APP.startSubWindow("Edit List Entry", "Edit", True)
    APP.setStretch("column")
    APP.setSticky("nsew")
    APP.addLabel("Program Index Label", "Index")
    APP.addLabelEntry("Name Entry")
    APP.addLabelDirectoryEntry("Program Location Entry")
    APP.addLabelDirectoryEntry("License Location Entry")
    APP.setStretch("both")
    APP.addLabelEntry("Notes Entry")
    APP.setStretch("column")
    APP.addButton("Submit changes", submit_list_entry_change)
    APP.stopSubWindow()


def create_warning_window():
    """
    Creates a window which can be used to display warnings and
    ask for confirmation.
    """
    APP.startSubWindow("Warning Window", "Warning", modal=True)
    APP.setSticky("nsew")
    APP.addLabel("Warning Message")
    APP.setStretch("column")
    APP.addButton("Confirm", warning_confirmed)
    APP.stopSubWindow()


def display_warning_message(warning: str):
    """
    Display the prepared "Warning Window" with a specified message
    """
    APP.setLabel("Warning Message", warning)
    APP.showSubWindow("Warning Window")


def warning_confirmed():
    """
    Hides the warning window.
    """
    APP.hideSubWindow("Warning Window")

def update_license_list():
    """
    Updates the ListBox that stores the license files
    """
    if APP.getListBox("Software List"):
        APP.updateListBox("License List", get_license_list())

def change_license_text(list_changed_event):
    """
    Updates the textBox that stores the license to show
    the license of the currently selected list entry.
    """
    try:
        license_location = license_directory + "/" + APP.getListBox("License List")[0]
    except IndexError:
        return

    APP.clearTextArea("License Text")
    try:
        with open(license_location, "r") as file:
            text = file.read()
        APP.setTextArea("License Text", text)
    except FileNotFoundError:
        print("Could not open " + license_location)
        APP.setTextArea("License Text", "Failed to open file.")


def submit_list_entry_change(event):
    """
    Accept changes to the list entry made by the user.
    The changes to be made are taken from the subwindow
    in which the user can make changes.
    """
    software_index = int(APP.getLabel("Program Index Label").split()[-1])
    software = CATALOG.get_software(software_index)
    software.name = APP.getEntry("Name Entry")
    software.program_location = APP.getEntry("Program Location Entry")
    software.license_location = APP.getEntry("License Location Entry")
    software.note = APP.getEntry("Notes Entry")

    if(software.license_location == "" or software.license_location is None):
        display_warning_message(
            "The license location is empty, " +
            "you will not be able to view or parse the license")

    CATALOG.update_software(software)
    APP.updateListBox(
        "Software List",
        get_software_list(),
        callFunction=False)
    APP.hideSubWindow("Edit List Entry")

def get_software_index() -> int:
    return int(APP.getListBox("Software List")[0].split()[0])

def edit_list_entry(event):
    """
    Change the subwindow in which the user can edit list entries
    to reflect the current contetns of the list entry that is selected.
    """
    index = get_software_index()
    software = CATALOG.get_software(index)
    APP.setLabel("Program Index Label", "Program Index: " + str(index))
    APP.setEntry("Name Entry", software.name)
    APP.setEntry("Program Location Entry", software.program_location)
    APP.setEntry("License Location Entry", software.license_location)
    APP.setEntry("Notes Entry", software.note)
    APP.showSubWindow("Edit List Entry")


def add_list_entry():
    """
    Adds an empty Program to the software catalog and then updates
    the list to reflect the change
    """
    CATALOG.add_software(SoftwareProgram("New Entry", "", "", ""))
    APP.updateListBox(
        "Software List",
        get_software_list(),
        select=True,
        callFunction=True)
    edit_list_entry(None)

def delete_list_entry():
    """
    Removes program from the software catalog and updates the list
    to reflect the change
    """
    CATALOG.delete_software(get_software_index())
    APP.updateListBox("Software List", get_software_list())

def parse_license():
    """
    Parse the text of the license that is currently stored
    inside the TextBox that displayes the license.
    """
    license_text = APP.getTextArea("License Text")
    ANALIZER.analyze_license_string(license_text)
    ANALIZER.open_analysis_in_browser()

def get_software_list():
    """
    Filters out software depending on booleans:
    hide_files_not_containing_paths and
    hide_files_not_containing_licenses

    Returns the list with filtered results 
    """
    software_list = CATALOG.list_installed_software()
    
    filtered_list = []
    for software in software_list:
        if hide_files_not_containing_paths:
            if software.program_location == "":
                continue
        if hide_files_not_containing_licenses:
            if software.license_location == "":
                continue
        if software_search_value.casefold() not in software.__str__().casefold():
            continue
        filtered_list.append(software)

    return filtered_list

def scan_for_software():
    """
    Use an tool that scans the computer in search for installed software.
    """
    global scanning_in_progress
    display_warning_message("Scanning started. This might last several minutes")
    import time
    execution_time = time.process_time()
    CATALOG.update_software_catalog()
    execution_time = time.process_time() - execution_time
    APP.updateListBox("Software List", get_software_list())
    scanning_in_progress = False
    display_warning_message("".join(["Scanning Complete.\n\nExecution Time = ", str(execution_time), "s"]))


def scan_in_spearate_thread():
    global scanning_in_progress
    if(scanning_in_progress):
        display_warning_message("Scanning in progress...")
    else:
        scanning_in_progress = True
        _thread.start_new_thread(scan_for_software, ())

def add_default_button(title, func, row=None, column=0, colspan=0, rowspan=0):
    """
    Add a button with sticky set to "ew" and stretch set to "column"
    """
    APP.setSticky("ew")
    APP.setStretch("column")
    return APP.addButton(title, func, row, column, colspan, rowspan)

def set_icon():
    """
    Sets icon to favicon.ico. If icon is not found sets it to None.
    """
    try:
        APP.icon = "favicon.ico"
    except Exception:
        APP.winIcon = None

def show_all_software():
    """
    Shows all software available
    """
    global hide_files_not_containing_paths
    global hide_files_not_containing_licenses
    hide_files_not_containing_paths = False
    hide_files_not_containing_licenses = False
    APP.updateListBox("Software List", get_software_list())

def show_software_without_paths():
    """
    Shows software with empty software_location
    """
    global hide_files_not_containing_paths
    hide_files_not_containing_paths = False
    APP.updateListBox("Software List", get_software_list())

def hide_software_without_paths():
    """
    Hides software with empty software_location
    """
    global hide_files_not_containing_paths
    hide_files_not_containing_paths = True
    APP.updateListBox("Software List", get_software_list())

def show_software_without_licenses():
    """
    Shows software with empty license_location
    """
    global hide_files_not_containing_licenses
    hide_files_not_containing_licenses = False
    APP.updateListBox("Software List", get_software_list())

def hide_software_without_licenses():
    """
    Hide software with empty license_location
    """
    global hide_files_not_containing_licenses
    hide_files_not_containing_licenses = True
    APP.updateListBox("Software List", get_software_list())

def add_search_entry(title, func, row=None, column=0, colspan=0, rowspan=0, secret=False):
    APP.setSticky("ew")
    APP.setStretch("column")
    APP.addEntry(title, row, column, colspan, rowspan, secret)
    APP.setEntryChangeFunction(title, func)

def update_software_search_value():
    global software_search_value
    software_search_value = APP.getEntry("Software Search Entry")
    APP.updateListBox("Software List", get_software_list())

def update_license_search_value():
    global license_search_value
    license_search_value = APP.getEntry("License Search Entry")
    APP.updateListBox("License List", get_license_list())


def main():
    """
    Run the GUI for the software organiser
    """
    set_icon()
    APP.startPanedFrame("p1", 0, 0, 2)
    APP.startPanedFrameVertical("pv1", 0, 0, 2)
    add_search_entry("Software Search Entry", update_software_search_value, 0, 0, 2)
    create_software_list(get_software_list(), 1, 0, 2)
    APP.startPanedFrame("pv2", 2, 0, 2)
    add_search_entry("License Search Entry", update_license_search_value, 2, 0, 2)
    create_license_list(3, 0, 2)
    add_default_button("Add Software", add_list_entry, 5, 0)
    add_default_button("Delete Software", delete_list_entry, 5, 1)
    APP.stopPanedFrame()
    APP.stopPanedFrame()
    APP.startPanedFrame("p2", 0, 1)
    create_license_box(0, 0, 2, 2)
    add_default_button("Parse License", parse_license, 1, 0)
    APP.stopAllPanedFrames()

    create_edit_window()
    create_warning_window()
    APP.addMenuList("Menu", ["Scan for Software"], [scan_in_spearate_thread])
    APP.addMenuList("View", ["Show all software",
                            None,
                            "Show software without software paths",
                            "Hide software without software paths",
                            None,
                            "Show software without license paths",
                            "Hide software without license paths"],
                            [show_all_software,
                            None,
                            show_software_without_paths,
                            hide_software_without_paths,
                            None,
                            show_software_without_licenses,
                            hide_software_without_licenses])
    APP.go()

if __name__ == "__main__":
    main()
