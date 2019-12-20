import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, qApp, QAction, QTextEdit
from PyQt5.QtGui import QIcon

class Bar(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建一个文字编辑的窗口
        text = QTextEdit()
        self.setCentralWidget(text)

        # 退出菜单
        exit_action = QAction(QIcon('迪迪003'), 'Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Be careful')

        exit_action.triggered.connect(qApp.quit)

        # 状态栏
        self.statusBar()

        # 菜单栏
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(exit_action)

        # 工具栏
        toolbar = self.addToolBar('Exit too')
        toolbar.addAction(exit_action)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('All together')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Bar()
    sys.exit(app.exec_())

