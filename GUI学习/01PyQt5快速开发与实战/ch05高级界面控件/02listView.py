import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListView, QMessageBox
from PyQt5.QtCore import QStringListModel

class ListViewDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QListView Demo")
        self.setGeometry(300, 300, 300, 200)
        layout = QVBoxLayout()

        # 创建存储一组字符串模型
        self.slm = QStringListModel()
        self.q_list = ['Item 1', 'Item 2', 'Item 3', 'Item 4']
        self.slm.setStringList(self.q_list)

        # 创建QListView表格，并添加模型
        self.list_view = QListView()
        self.list_view.setModel(self.slm)
        self.list_view.clicked.connect(self.list_clicked)

        layout.addWidget(self.list_view)
        self.setLayout(layout)

    def list_clicked(self, q_model_index):
        QMessageBox.information(self, "ListWidget", "你选择了：{}"
                                .format(self.q_list[q_model_index.row()]))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = ListViewDemo()
    my_show.show()
    sys.exit(app.exec_())


