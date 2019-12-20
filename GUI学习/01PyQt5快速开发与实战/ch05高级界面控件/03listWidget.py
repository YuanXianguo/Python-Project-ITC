import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QMessageBox

class ListWidgetDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QListWidget Demo")
        self.setGeometry(300, 300, 300, 200)
        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        self.list_widget.addItems(['Item 1', 'Item 2', 'Item 3', 'Item 4'])
        self.list_widget.itemClicked.connect(self.list_clicked)

        layout.addWidget(self.list_widget)
        self.setLayout(layout)

    def list_clicked(self, item):
        QMessageBox.information(self, "ListWidget", "你选择了：{}"
                                .format(item.text()))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = ListWidgetDemo()
    my_show.show()
    sys.exit(app.exec_())


