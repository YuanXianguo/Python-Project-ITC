import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton
from PyQt5 import QtCore


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('自定义参数例子')
        self.setGeometry(300, 300, 300, 200)
        layout = QHBoxLayout()

        self.ok_btn = QPushButton('OK', self)
        # 使用setObjectName设置对象名称
        self.ok_btn.setObjectName('ok_button')
        layout.addWidget(self.ok_btn)
        self.setLayout(layout)

        QtCore.QMetaObject.connectSlotsByName(self)

    @QtCore.pyqtSlot()
    def on_ok_button_clicked(self):
        print('单击了OK按钮')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = Main()
    my_show.show()
    sys.exit(app.exec_())




