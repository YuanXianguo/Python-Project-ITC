import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout

class BoxLayout(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        ok_button = QPushButton('Ok')
        cancel_button = QPushButton('Cancel')

        h_box = QHBoxLayout()
        h_box.addStretch()
        h_box.addWidget(ok_button)
        h_box.addWidget(cancel_button)

        v_box = QVBoxLayout()
        v_box.addStretch()
        v_box.addLayout(h_box)

        self.setLayout(v_box)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Layout Management')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BoxLayout()
    sys.exit(app.exec_())
