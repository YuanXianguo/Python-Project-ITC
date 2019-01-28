import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt

from data_set import Ui_DataSet
from input_numeric_type import InputNumericType  # 导入数值型键盘类


class DataSet(QWidget, Ui_DataSet):
    """配方列表"""

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('数据导出设定')
        self.width_, self.height_ = 800, 320
        self.setting()
        self.data_set_process()

    def setting(self):
        self.screen_rect = QApplication.desktop().screenGeometry()  # 获取显示器分辨率大小
        self.screen_height = self.screen_rect.height()
        self.screen_width = self.screen_rect.width()
        self.setGeometry((self.screen_width - self.width_) // 2, (self.screen_height - self.height_) // 2, self.width_, self.height_)
        self.setWindowModality(Qt.ApplicationModal)  # 应用程序模态，程序未完成当前对话框时，阻止和任何其他窗口进行交互
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        # self.setWindowFlags(Qt.CustomizeWindowHint)  # 隐藏标题
        self.setFixedSize(self.width(), self.height())  # 禁止拉伸窗口大小

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
