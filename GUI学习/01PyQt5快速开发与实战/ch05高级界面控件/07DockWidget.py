import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout,QDockWidget, QListWidget, QTextEdit
from PyQt5.QtCore import Qt

class DockWidgetDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DockWidget Demo")
        self.setGeometry(300, 300, 300, 200)
        layout = QVBoxLayout()

        bar = self.menuBar()
        file = bar.addMenu('File')
        file.addAction('New')
        file.addAction('Save')
        file.addAction('Quit')

        # 创建可停靠的窗口items
        self.items = QDockWidget('Dockable', self)
        self.list_widget = QListWidget()
        self.list_widget.addItems(['item1', 'item2', 'item3'])
        # 在停靠窗口items内添加QListWidget对象
        self.items.setWidget(self.list_widget)
        #self.items.setFloating(False)
        # 设置中央小控件为QTextEdit对象
        self.setCentralWidget(QTextEdit())
        # 将停靠窗口放置在中央小控件的右侧
        self.addDockWidget(Qt.RightDockWidgetArea, self.items)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = DockWidgetDemo()
    my_show.show()
    sys.exit(app.exec_())
