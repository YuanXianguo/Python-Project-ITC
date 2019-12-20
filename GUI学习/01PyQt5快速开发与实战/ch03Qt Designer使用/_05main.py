import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from _05MainForm import Ui_MainWindow

class MyForm(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 菜单的点击事件，当点击关闭菜单时连接槽函数close()
        self.actionfileClose.triggered.connect(self.close)
        # 菜单的点击事件，当点击打开菜单时连接槽函数open_msg()
        self.actionfileOpen.triggered.connect(self.open_msg)

    def open_msg(self):
        file, ok = QFileDialog.getOpenFileName(self, "打开",
                        "C:/", "All Files (*);;Text Files(*.txt)")
        # 在状态栏显示文件地址
        self.statusBar().showMessage(file)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_form = MyForm()
    my_form.show()
    sys.exit(app.exec_())

