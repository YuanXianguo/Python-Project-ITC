import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

class QMessageBoxDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QMessageBox demo")
        self.setGeometry(300, 300, 300, 200)

        self.btn = QPushButton("弹出对话框", self)
        self.btn.move(50, 50)
        self.btn.clicked.connect(self.show_message)

    def show_message(self):
        # 使用information信息框
        QMessageBox.information(self, "标题", "消息正文",
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = QMessageBoxDemo()
    my_show.show()
    sys.exit(app.exec_())
