import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea, QAction, QMdiSubWindow, QTextEdit


class MainWindowDemo(QMainWindow):
    count = 0

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MDI Demo")
        self.setGeometry(300, 300, 500, 300)

        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)

        bar = self.menuBar()
        file = bar.addMenu('File')
        file.addAction('New')
        file.addAction('Cascade')
        file.addAction('Tiled')
        file.triggered[QAction].connect(self.window_action)

    def window_action(self, q):
        if q.text() == 'New':
            MainWindowDemo.count = MainWindowDemo.count + 1
            sub = QMdiSubWindow()
            sub.setWidget(QTextEdit())
            sub.setWindowTitle('subwindow ' + str(MainWindowDemo.count))
            self.mdi.addSubWindow(sub)
            sub.show()
        if q.text() == 'Cascade':
            self.mdi.cascadeSubWindows()
        if q.text() == 'Tiled':
            self.mdi.tileSubWindows()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = MainWindowDemo()
    my_show.show()
    sys.exit(app.exec_())
