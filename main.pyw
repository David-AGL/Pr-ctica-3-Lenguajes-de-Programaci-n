import sys
from PyQt5 import QtWidgets
from logic import Ui_Interface

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Interface = QtWidgets.QWidget()
    ui = Ui_Interface()
    ui.setupUi(Interface)
    Interface.show()
    sys.exit(app.exec_())
