from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent
import sys
from input_name import Ui_input_name


class InputName(QWidget, Ui_input_name):
    """名字输入"""

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.width_, self.height_ = 660, 300
        self.setting()
        self.input_name_process()

    def setting(self):
        self.screen_rect = QApplication.desktop().screenGeometry()  # 获取显示器分辨率大小
        self.screen_height = self.screen_rect.height()
        self.screen_width = self.screen_rect.width()
        self.setGeometry((self.screen_width - self.width_) // 2,
                         (self.screen_height - self.height_) // 2, self.width_, self.height_)
        self.setWindowModality(Qt.ApplicationModal)  # 应用程序模态，程序未完成当前对话框时，阻止和任何其他窗口进行交互
        self.setWindowFlags(Qt.CustomizeWindowHint)  # 隐藏标题
        self.setFixedSize(self.width(), self.height())  # 禁止拉伸窗口大小

    def input_name_process(self):
        """处理函数"""
        self.lineEdit_input.installEventFilter(self)  # 添加事件过滤器
        self.lowered = 0  # 判断是否显示的小写
        self.has_selected = 1  # 判断输入框是否有被选择的文本
        self.btn_input_list = []  # 存储所有的按键
        for i in range(38):
            self.btn_input_list.append('self.btn_input_{}'.format(i))
        for i in self.btn_input_list:
            eval(i).clicked.connect(self.lineEdit_input_show)
        self.btn_input_back.clicked.connect(self.lineEdit_input_back)
        self.btn_input_clear.clicked.connect(self.lineEdit_input_clear)
        self.btn_input_cancel.clicked.connect(self.close)
        self.btn_input_another.clicked.connect(self.another_show)

    def another_show(self):
        self.upper_show() if self.lowered else self.lower_show()

    def lower_show(self):
        for i in self.btn_input_list[12:38]:
            text = chr(ord(eval(i).text()) + 32)
            eval(i).setText(text)
        self.btn_input_another.setText('大写')
        self.lowered = 1

    def upper_show(self):
        for i in self.btn_input_list[12:38]:
            text = chr(ord(eval(i).text()) - 32)
            eval(i).setText(text)
        self.btn_input_another.setText('小写')
        self.lowered = 0

    def lineEdit_input_show(self):
        sender = self.sender()
        text = self.lineEdit_input.text()
        cursor_index = self.lineEdit_input.cursorPosition()  # 判断光标位置
        if self.has_selected == 1:  # 如果有被选择文本
            text1 = sender.text()
            self.has_selected = 0
        else:  # 将输入文本插入光标位置
            text1 = text[:cursor_index] + sender.text() + text[cursor_index:]
        self.lineEdit_input.setText(text1)
        self.lineEdit_input.setCursorPosition(cursor_index + 1)  # 光标后移1位

    def lineEdit_input_back(self):
        cursor_index = self.lineEdit_input.cursorPosition()
        text = self.lineEdit_input.text()
        self.lineEdit_input.setText(text[:cursor_index - 1] + text[cursor_index:])
        self.lineEdit_input.setCursorPosition(cursor_index - 1)

    def lineEdit_input_clear(self):
        self.lineEdit_input.clear()

    def eventFilter(self, object, event):
        """给lineEdit添加单击左键事件过滤器"""
        if object == self.lineEdit_input:
            if event.type() == QMouseEvent.MouseButtonPress:
                mouse_event = QMouseEvent(event)
                if mouse_event.buttons() == Qt.LeftButton:
                    self.has_selected = 0
        return QWidget.eventFilter(self, object, event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = InputName()
    my_show.show()
    sys.exit(app.exec_())

