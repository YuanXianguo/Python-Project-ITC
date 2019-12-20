import sys
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap

class Form(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Button demo例子")
        layout = QVBoxLayout()

        # 设置按钮1
        self.btn1 = QPushButton('Button1')
        self.btn1.setCheckable(True) # 设置按钮已点击和释放状态
        # self.btn1.toggle() # 在按钮状态之间进行切换
        self.btn1.clicked.connect(self.btn_state)
        self.btn1.clicked.connect(lambda: self.which_btn(self.btn1))
        layout.addWidget(self.btn1)
        # 设置按钮2
        self.btn2 = QPushButton('image')
        self.btn2.setIcon(QIcon(QPixmap("pangdi.jpg"))) # 设置图片
        self.btn2.clicked.connect(lambda: self.which_btn(self.btn2))
        layout.addWidget(self.btn2)
        # 设置按钮3
        self.btn3 = QPushButton('Disabled')
        self.btn3.setEnabled(False) # 设置状态不可用
        layout.addWidget(self.btn3)
        # 设置按钮4
        self.btn4 = QPushButton('&Download')
        self.btn4.setDefault(True) # 设置按钮的默认状态
        self.btn4.clicked.connect(lambda: self.which_btn(self.btn4))
        layout.addWidget(self.btn4)
        self.setLayout(layout)

    def btn_state(self):
        # 返回按钮的状态，True或False
        if self.btn1.isChecked():
            print("button pressed")
        else:
            print("button released")

    def which_btn(self, btn):
        print("clicked button is " + btn.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = Form()
    my_show.show()
    sys.exit(app.exec_())
