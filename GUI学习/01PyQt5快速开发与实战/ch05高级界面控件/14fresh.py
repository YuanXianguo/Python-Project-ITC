import sys, time
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QListWidget

class freshDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('实时刷新页面例子')
        layout = QGridLayout()

        self.list_file = QListWidget()
        self.start_btn = QPushButton('开始')
        layout.addWidget(self.list_file, 0, 0, 1, 2)
        layout.addWidget(self.start_btn, 1, 1)
        self.start_btn.clicked.connect(self.slot_add)

        self.setLayout(layout)

    def slot_add(self):
        for n in range(10):
            str_n = 'File index{}'.format(n)
            self.list_file.addItem(str_n)
            QApplication.processEvents()
            time.sleep(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = freshDemo()
    my_show.show()
    sys.exit(app.exec_())
