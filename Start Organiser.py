
import sys
sys.path.append("src")
import qt_gui as gui

args = sys.argv
if len(args) == 1:
    args.append('-style')
    args.append('Fusion')
gui.main(sys.argv)
