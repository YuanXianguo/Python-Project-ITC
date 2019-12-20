import sys
from PyQt5.QtWidgets import QApplication, QWidget
from login import Ui_Form

class Mywindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = Mywindow()
    my_show.show()
    sys.exit(app.exec_())
