from mainwindow import MainWindow

def main(argv):
	from PySide2.QtWidgets import QApplication
	from PySide2.QtCore import Qt, QCoreApplication
	# QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
	a = QApplication(argv)
	w = MainWindow()
	w.show()
	return a.exec_()

if __name__ == "__main__":
	import sys
	main(sys.argv)