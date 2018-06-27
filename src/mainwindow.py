import sys

import _thread

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QMainWindow, QTreeWidgetItem, QMessageBox
from PySide2.QtCore import QFile

from software_program import SoftwareProgram
from software_license_organiser import SoftwareLicenseOrganiser
from license_web_analyzer import LicenseWebAnalyzer


class MainWindow:
	def __init__(self):
		self.setup_ui()
		self.setup_signals()
		self.setup_class_variables()
		self.update_software_tree()

	def setup_ui(self):
		import os
		directory = os.path.dirname(os.path.realpath(__file__))
		uiLoader = QUiLoader()
		uiFile = QFile(directory + "\\mainwindow.ui")
		uiFile.open(QFile.ReadOnly)
		self.ui = uiLoader.load(uiFile)
		uiFile.close()

	def setup_signals(self):
		self.ui.actionScan_for_software.triggered.connect(self.on_actionScan_for_software_triggered)
		self.ui.actionShow_all_software.triggered.connect(self.on_actionShow_all_software_triggered)
		self.ui.actionHide_software_without_path.toggled.connect(self.on_actionHide_software_without_path_toggled)
		self.ui.actionHide_software_without_license.toggled.connect(self.on_actionHide_software_without_license_toggled)
		self.ui.softwareTreeWidget.itemSelectionChanged.connect(self.on_softwareTreeWidget_itemSelectionChanged)
		self.ui.licenseListWidget.itemSelectionChanged.connect(self.on_licenseListWidget_itemSelectionChanged)
		self.ui.addSoftwareButton.clicked.connect(self.on_addSoftwareButton_clicked)
		self.ui.removeSoftwareButton.clicked.connect(self.on_removeSoftwareButton_clicked)
		self.ui.parseLicenseButton.clicked.connect(self.on_parseLicenseButton_clicked)
		self.ui.softwareSearchLineEdit.textChanged.connect(self.on_softwareSearchLineEdit_textChanged)
		self.ui.licenseSearchLineEdit.textChanged.connect(self.on_licenseSearchLineEdit_textChanged)

	def setup_class_variables(self):
		self.CATALOG = SoftwareLicenseOrganiser("softwares.pi")
		self.ANALIZER = LicenseWebAnalyzer()
		self.scanning_in_progress = False
		self.hide_files_not_containing_paths = False
		self.hide_files_not_containing_licenses = False
		self.software_search_text = ""
		self.license_search_text = ""
		self.software_list = self.CATALOG.list_installed_software()

	def update_software_tree(self):
		self.ui.softwareTreeWidget.clear()
		for software in self.software_list:
			if self.hide_files_not_containing_paths:
				if software.program_location == "":
					continue
					
			if self.hide_files_not_containing_licenses:
				if software.license_location == "":
					continue
					
			if self.software_search_text.casefold() not in software.__str__().casefold():
				continue
			
			item = QTreeWidgetItem()
			item.setText(0, software.name)
			self.insertChildren(item, software)
			self.ui.softwareTreeWidget.addTopLevelItem(item)

	def insertChildren(self, item, software):
		item.insertChild(0, self.getIndexItem(software))
		item.insertChild(1, self.getNameItem(software))
		item.insertChild(2, self.getDirectoryItem(software))
		item.insertChild(3, self.getLicenseDirItem(software))
		item.insertChild(4, self.getNoteItem(software))

	def getIndexItem(self, software):
		return self.getSubItem("Index", str(software.index))

	def getNameItem(self, software):
		return self.getSubItem("Name", software.name)

	def getDirectoryItem(self, software):
		return self.getSubItem("Directory", software.program_location)

	def getLicenseDirItem(self, software):
		return self.getSubItem("License Dir", software.license_location)

	def getNoteItem(self, software):
		return self.getSubItem("Note", software.note)

	def getSubItem(self, name, value):
		subItem = QTreeWidgetItem()
		subItem.setText(0, name)
		subItem.setText(1, value)
		return subItem


	def add_software(self):
		pass

	def remove_software(self):
		pass

	def update_license_list(self):
		item = self.ui.softwareTreeWidget.currentItem()
		if not item:
			self.ui.licenseListWidget.clear()
			return

		while item.parent():
			item = item.parent()

		index = self.ui.softwareTreeWidget.indexOfTopLevelItem(item)
		software = self.CATALOG.get_software(index)
		
		license_files = []
		if software:
			if software.license_location != "":
				import os, glob
				if os.path.isdir(software.license_location):
					license_files.extend(os.path.basename(license_file) for license_file in glob.iglob("".join([software.license_location, "/*"])))
				elif os.path.isfile(software.license_location):
					license_files.append(os.path.basename(software.license_location))

				for index, license_file in enumerate(license_files.copy()):
					if self.license_search_text.casefold() not in license_file.casefold():
						del license_files[index]

		self.ui.licenseListWidget.clear()
		self.ui.licenseListWidget.addItems(license_files)

	def update_license_plain_text_edit(self):
		item = self.ui.softwareTreeWidget.currentItem()
		if not item:
			self.ui.licensePlainTextEdit.setPlainText("")
		
		while item.parent():
			item = item.parent()

		index = self.ui.softwareTreeWidget.indexOfTopLevelItem(item)
		software = self.CATALOG.get_software(index)
		
		license_name = self.ui.licenseListWidget.currentItem().text()
		if license_name == "":
			self.ui.licensePlainTextEdit.setPlainText("")
			return

		import os.path
		if os.path.isdir(software.license_location):
			license_path = software.license_location + "/" + license_name
		elif os.path.isfile(software.license_location):
			license_path = software.license_location
		else:
			self.ui.licensePlainTextEdit.setPlainText("")
			return

		try:
			with open(license_path, "r") as license_file:
				text = license_file.read()
			self.ui.licensePlainTextEdit.setPlainText(text)
		except FileNotFoundError:
			print("Could not open " + license_path)
			self.ui.licensePlainTextEdit.setPlainText("Failed to open file")

	def on_actionShow_all_software_triggered(self):
		self.ui.actionHide_software_without_license.setChecked(False)
		self.ui.actionHide_software_without_path.setChecked(False)

	def on_actionHide_software_without_path_toggled(self, selection):
		self.hide_files_not_containing_paths = selection
		self.update_software_tree()

	def on_actionHide_software_without_license_toggled(self, selection):
		self.hide_files_not_containing_licenses = selection
		self.update_software_tree()

	def on_softwareTreeWidget_itemSelectionChanged(self):
		self.update_license_list()

	def on_licenseListWidget_itemSelectionChanged(self):
		self.update_license_plain_text_edit()

	def on_addSoftwareButton_clicked(self):
		pass

	def on_removeSoftwareButton_clicked(self):
		pass

	def on_parseLicenseButton_clicked(self):
		license_text = self.ui.licensePlainTextEdit.toPlainText()
		self.ANALIZER.analyze_license_string(license_text)
		self.ANALIZER.open_analysis_in_browser()

	def on_actionScan_for_software_triggered(self):
		self.scan_in_spearate_thread()

	def scan_in_spearate_thread(self):
		if(self.scanning_in_progress):
			self.display_warning_message("Scanning in progress...")
		else:
			self.scanning_in_progress = True
			_thread.start_new_thread(self.scan_for_software, ())

	def scan_for_software(self):
		self.display_warning_message("Scanning started. This might last several minutes")
		import time
		execution_time = time.process_time()
		self.CATALOG.update_software_catalog()
		execution_time = time.process_time() - execution_time
		self.update_software_tree()
		self.scanning_in_progress = False
		self.display_warning_message("".join(["Scanning Complete.\n\nExecution Time = ", str(execution_time), "s"]))

	def display_warning_message(self, msg):
		return
		msg_box = QMessageBox(self.ui)
		msg_box.setWindowTitle("Warning")
		msg_box.setText("This is a message")
		msg_box.exec_()

	def on_softwareSearchLineEdit_textChanged(self, text):
		self.software_search_text = text
		self.update_software_tree()

	def on_licenseSearchLineEdit_textChanged(self, text):
		self.license_search_text = text
		self.update_license_list()

	def show(self):
		self.ui.show()

	def close(self):
		self.ui.close()
		sys.exit(0)

if __name__ == "__main__":
	from PySide2.QtWidgets import QApplication
	app = QApplication(sys.argv)

	window = MainWindow()
	window.show()

	sys.exit(app.exec_())