import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDialog
from PyQt5.QtCore import Qt

class DialogDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dialog demo")
        self.setGeometry(300, 300, 300, 200)

        self.btn = QPushButton("弹出对话框", self)
        self.btn.move(50, 50)
        self.btn.clicked.connect(self.show_dialog)

    def show_dialog(self):
        dialog = QDialog()
        btn = QPushButton("ok", dialog)
        btn.move(50, 50)
        dialog.setWindowTitle("Dialog")
        # 设置为应用程序模态，阻止和任何其他窗口进行交互
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = DialogDemo()
    my_show.show()
    sys.exit(app.exec_())
