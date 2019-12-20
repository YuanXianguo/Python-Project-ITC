import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFormLayout, QLineEdit, QLabel, QComboBox

class dragDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("drag Demo")
        self.setGeometry(300, 300, 300, 200)
        layout = QFormLayout()
        layout.addRow(QLabel('请把左边的文本拖拽到右边的下拉菜单中'))
        le = QLineEdit()
        le.setDragEnabled(True)
        com = Combo('Button', self)
        layout.addRow(le, com)
        self.setLayout(layout)

class Combo(QComboBox):
    def __init__(self, title, parent):
        super().__init__()
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.addItem(e.mimeData().text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = dragDemo()
    my_show.show()
    sys.exit(app.exec_())
