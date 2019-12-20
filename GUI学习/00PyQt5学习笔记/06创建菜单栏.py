import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, qApp, QAction
from PyQt5.QtGui import QIcon

class Menubar(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建一个退出菜单exit_action，并创建快捷键Ctrl+Q
        exit_action = QAction(QIcon('迪迪003'), 'Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Press and quit')

        exit_action.triggered.connect(qApp.quit)

        # 状态栏
        self.statusBar()

        # 创建这个菜单栏，上面附加了一个名为'File'的菜单，添加退出菜单exit_action
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(exit_action)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Menubar')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menubar()
    sys.exit(app.exec_())

