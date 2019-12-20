import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction
from PyQt5.QtGui import QIcon

class ToolBarDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ToolBar Demo")
        self.setGeometry(300, 300, 300, 200)

        # 在工具栏区域添加文件工具栏
        tb = self.addToolBar('File')

        # 添加具有文本标题的工具按钮，工具栏通常包含图形按钮
        # 具有图标和名称的QAction对象将被添加到工具栏中
        new = QAction(QIcon('pangdi.jpg'), 'new', self)
        tb.addAction(new)
        open = QAction(QIcon('pangdi.jpg'), 'open', self)
        tb.addAction(open)
        save = QAction(QIcon('pangdi.jpg'), 'save', self)
        tb.addAction(save)

        tb.actionTriggered[QAction].connect(self.process_trigger)

    def process_trigger(self, q):
        print("{} is triggered".format(q.text()))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = ToolBarDemo()
    my_show.show()
    sys.exit(app.exec_())
