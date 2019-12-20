import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

class BtnClicked(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        btn1 = QPushButton('Hello', self)
        btn2 = QPushButton('world', self)

        btn1.move(30, 150)
        btn2.move(150, 150)

        btn1.clicked.connect(self.btn_clicked)
        btn2.clicked.connect(self.btn_clicked)

        self.statusBar()

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('sender')
        self.show()

    def btn_clicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' was clicked')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BtnClicked()
    sys.exit(app.exec_())
