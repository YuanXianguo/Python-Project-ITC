import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class freshDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(5, 30, 1355, 730)
        self.setWindowTitle('打开外部网页例子')

        self.browser = QWebEngineView()
        # 加载外部的Web页面
        self.browser.load(QUrl('http://www.baidu.com'))
        self.setCentralWidget(self.browser)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = freshDemo()
    my_show.show()
    sys.exit(app.exec_())
