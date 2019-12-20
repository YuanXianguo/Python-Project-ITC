import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QPushButton

class WinForm(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("关闭主窗口例子")
        self.resize(300, 200)
        self.button1 = QPushButton("关闭主窗口")
        self.button1.clicked.connect(self.onButtonClick)

        layout = QHBoxLayout()
        layout.addWidget(self.button1)

        main_frame = QWidget()
        main_frame.setLayout(layout)
        self.setCentralWidget(main_frame)

    def onButtonClick(self):
        # sender是发送信号的对象,此处是button1
        sender = self.sender()
        print(sender.text() + '被按下了')
        qApp = QApplication.instance()
        qApp.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = WinForm()
    my_show.show()
    sys.exit(app.exec_())

