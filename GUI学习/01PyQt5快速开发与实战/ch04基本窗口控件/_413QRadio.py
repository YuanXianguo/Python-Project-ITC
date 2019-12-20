import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QRadioButton

class Radiodemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RadioButton demo")
        self.setGeometry(300, 300, 300, 200)
        layout = QHBoxLayout()

        self.btn1 = QRadioButton("Button1")
        self.btn1.setChecked(True)
        self.btn1.toggled.connect(lambda: self.btn_state(self.btn1))
        layout.addWidget(self.btn1)

        self.btn2 = QRadioButton("Button2")
        self.btn2.toggled.connect(lambda: self.btn_state(self.btn2))
        layout.addWidget(self.btn2)

        self.setLayout(layout)

    def btn_state(self, btn):
        if btn.isChecked():
            print(btn.text() + " is selected")
        else:
            print(btn.text() + " is deselected")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = Radiodemo()
    my_show.show()
    sys.exit(app.exec_())
