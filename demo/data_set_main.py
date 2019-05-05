import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt

from data_set import Ui_DataSet
from input_numeric_type import InputNumericType  # 导入数值型键盘类
import settings


class DataSet(QWidget, Ui_DataSet):
    """配方列表"""

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('数据导出设定')
        self.width_, self.height_ = 800, 320
        settings.get_set(self)
        self.data_set_process()

    def data_set_process(self):
        self.btn_data_process_cancel.clicked.connect(self.data_set_exit)

    def data_set_exit(self):
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = DataSet()
    my_show.show()
    sys.exit(app.exec_())
