import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QTextEdit, QStatusBar


class StatusBarDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StatusBar Demo")
        self.setGeometry(300, 300, 300, 200)

        bar = self.menuBar()
        file = bar.addMenu('File')
        file.addAction('show')
        file.triggered[QAction].connect(self.process_trigger)
        self.setCentralWidget(QTextEdit())

        # 设置状态栏
        self.sb = QStatusBar()
        self.setStatusBar(self.sb)

    def process_trigger(self, q):
        if (q.text() == 'show'):
            self.sb.showMessage("{}菜单选项被点击了".format(q.text()), 5000)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = StatusBarDemo()
    my_show.show()
    sys.exit(app.exec_())
