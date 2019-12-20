import sys
from PyQt5.QtWidgets import QApplication, QWidget
from _07MainWin02 import Ui_Form

class MainForm(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = MainForm()
    my_show.show()
    sys.exit(app.exec_())
