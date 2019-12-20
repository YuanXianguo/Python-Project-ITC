import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction

class MenuDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu Demo")
        self.setGeometry(300, 300, 300, 200)

        # 顶层窗口必须时QMainWindow对象，才可以引用QMenuBar对象
        bar = self.menuBar()

        # 在菜单栏中添加"File"菜单
        file = bar.addMenu('File')

        # 菜单中的操作按钮可以是字符串或QAction对象
        # 在"File"菜单中添加操作按钮
        file.addAction('New')
        save = QAction('Save', self)
        save.setShortcut('Ctrl+S')
        file.addAction(save)
        quit = QAction('Quit', self)
        file.addAction(quit)
        # 在顶级菜单"File"中添加将子菜单"Edit"
        edit = file.addMenu('Edit')
        edit.addAction('Copy')
        edit.addAction('Paste')
        file.triggered[QAction].connect(self.process_trigger)

    def process_trigger(self, q):
        print("{} is triggered".format(q.text()))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = MenuDemo()
    my_show.show()
    sys.exit(app.exec_())
