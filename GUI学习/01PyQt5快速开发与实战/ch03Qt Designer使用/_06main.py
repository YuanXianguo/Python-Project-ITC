import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog
from _06MainForm2 import Ui_MainWindow
from _06ChildrenForm2 import Ui_ChildrenForm

class MainForm(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 菜单的点击事件，当点击关闭菜单时连接槽函数close()
        self.actionfileClose.triggered.connect(self.close)
        # 菜单的点击事件，当点击打开菜单时连接槽函数open_msg()
        self.actionfileOpen.triggered.connect(self.open_msg)

        # 实例化一个子窗口
        self.child = ChildrenForm()

        # 单击新建窗体，子窗口就会显示在主窗口的MaingridLayout中
        self.addWinAction.triggered.connect(self.child_show)

    def child_show(self):
        # 添加子窗口
        self.MaingridLayout.addWidget(self.child)
        self.child.show()

    def open_msg(self):
        file, ok = QFileDialog.getOpenFileName(self, "打开",
                              "C:/", "All Files (*);;Text Files(*.txt")
        # 在状态栏显示文件地址
        self.statusBar().showMessage(file)

class ChildrenForm(QWidget, Ui_ChildrenForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = MainForm()
    my_show.show()
    sys.exit(app.exec_())
