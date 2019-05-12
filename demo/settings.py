from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt


def setting(self):
    # 获取显示器分辨率大小
    self.screen_rect = QApplication.desktop().screenGeometry()
    self.screen_height = self.screen_rect.height()
    self.screen_width = self.screen_rect.width()
    self.setGeometry((self.screen_width - self.width_) // 2,
                     (self.screen_height - self.height_) // 2,
                     self.width_, self.height_)
    # 应用程序模态，程序未完成当前对话框时，阻止和任何其他窗口进行交互
    self.setWindowModality(Qt.ApplicationModal)
    self.setWindowFlags(Qt.CustomizeWindowHint)  # 隐藏标题
    self.setFixedSize(self.width(), self.height())  # 禁止拉伸窗口大小
