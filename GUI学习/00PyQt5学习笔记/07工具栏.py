import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, qApp, QAction
from PyQt5.QtGui import QIcon

class Toolbar(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 退出菜单
        exit_action = QAction(QIcon('迪迪003'), 'Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Be careful')

        exit_action.triggered.connect(qApp.quit)

        # 状态栏
        self.statusBar()

        # 将退出动作添加到工具栏里，同时当鼠标悬浮到工具栏的按钮时，底部的状态栏会提示'Be careful'
        toolbar = self.addToolBar('Exit too')
        toolbar.addAction(exit_action)


        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Toolbar')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Toolbar()
    sys.exit(app.exec_())

