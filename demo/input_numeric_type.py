import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent

from input_numeric import Ui_InputNumericType


class InputNumericType(QWidget, Ui_InputNumericType):
    """数值型输入"""

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.width_, self.height_ = 660, 200
        self.setting()
        self.input_numeric_process()

    def setting(self):
        self.screen_rect = QApplication.desktop().screenGeometry()  # 获取显示器分辨率大小
        self.screen_height = self.screen_rect.height()
        self.screen_width = self.screen_rect.width()
        self.setGeometry((self.screen_width - self.width_) // 2, (self.screen_height - self.height_) // 2, self.width_, self.height_)
        self.setWindowModality(Qt.ApplicationModal)  # 应用程序模态，程序未完成当前对话框时，阻止和任何其他窗口进行交互
        self.setWindowFlags(Qt.CustomizeWindowHint)  # 隐藏标题
        self.setFixedSize(self.width(), self.height())  # 禁止拉伸窗口大小

    def input_numeric_process(self):
        """处理函数"""
        self.lineEdit_input.installEventFilter(self)  # 添加事件过滤器
        self.has_selected = 1  # 判断输入框是否有被选择的文本
        self.btn_input_list = []  # 存储所有的按键
        for i in range(12):
            self.btn_input_list.append('self.btn_input_{}'.format(i))
        for i in self.btn_input_list:
            eval(i).clicked.connect(self.lineEdit_input_show)
        self.btn_input_back.clicked.connect(self.lineEdit_input_back)
        self.btn_input_clear.clicked.connect(self.lineEdit_input_clear)
        self.btn_input_cancel.clicked.connect(self.close)

    def lineEdit_input_modify(self):
        """对文本进行格式化"""
        text = self.lineEdit_input.text()
        text = '0' if text == '' else text
        text = '-' + self.lineEdit_input_modify_(text[1:]) if text[0] == '-' else self.lineEdit_input_modify_(text)
        return text

    def lineEdit_input_modify_(self, text):
        """对去掉首位负号的文本进行格式化"""
        # 首位负号已经去掉，所以不能再出现，小数点只能出现一次
        text = text[:text.index('-')] if '-' in text else text
        if '.' in text:
            text_list = text.split('.')
            text = text_list[0] + '.' + text_list[1]
        text = text.lstrip('0')  # 去掉前面无效的0
        text = '0' if text == '' else text
        text = '0' + text if text[0] == '.' else text
        text = self.text_len7(text) if len(text) > 6 else text  # 文本长度大于6时保留6位有效数字,遵循四舍五入法，并引入科学记数法
        return text

    def text_len7(self, text):
        """文本长度大于6时保留6位有效数字,遵循四舍五入法，并引入科学记数法"""
        text = self.text_format(text)
        text1 = text[:7] if len(text) > 10 else text  # 同时处理计算机误差和小数点后多余的0
        text1 = text1.rstrip('.0') if '.' in text1 else text1  # 删除无效的小数点和0
        text = text1 + text[-4:] if len(text) > 10 and 'e' in text else text1
        return text

    def text_format(self, text):
        """ .format()方法只能保留小数点后6位，所以采用将小数点分别左移右移保证在(0,1)之间，格式化之后再复位"""
        text = text + '.' if '.' not in text else text
        dot_index = text.index('.')
        not_0_index = 0  # 计算小于1时第一个非0在第几位
        for i in text:
            if i not in ['0', '.']:
                break
            not_0_index += 1
        n = dot_index  # 大于等于1需要左移至(0,1)区间；以1.0为例，dot_index=1，左移n为1，从而可推出n表达式
        m = not_0_index - 2  # 小于1需要右移至(0,1)区间；以0.1为例，not_0_index为2，右移m为0，从而可推出m表达式
        # if dot_index > not_0_index 小数点在第一个非0之前表示小于1
        text = eval(text) * pow(10, -n) if dot_index > not_0_index else eval(text) * pow(10, m)  # 将小数点分别左移右移
        text = '{:.6f}'.format(text)  # 保留6位小数
        text = eval(text) * pow(10, n) if dot_index > not_0_index else eval(text) * pow(10, -m)  # 小数点复位
        text = '{:.5e}'.format(text) if dot_index > 6 else str(text)  # 对大于e+6的用科学记数法表示
        return text

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
    my_show = InputNumericType()
    my_show.show()
    sys.exit(app.exec_())
