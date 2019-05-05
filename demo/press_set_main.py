import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent, QFont

from press_set import Ui_PressSet
from input_numeric_type import InputNumericType  # 导入数值型键盘类


class PressSet(QWidget, Ui_PressSet):
    """压力设定"""

    def __init__(self, unit, work_pos_index, language):
        super().__init__()
        self.setupUi(self)
        self.width_, self.height_ = 310, 200
        self.unit = unit
        self.work_pos_index = work_pos_index
        self.language = language
        self.set_title()
        self.setting()
        self.press_set_process()

    def set_title(self):
        if self.unit == 'Pa':
            press_name = ['差压', 'different pressure'.upper()][self.language]
        else:
            press_name = ['表压', 'pressure'.upper()][self.language]
        if self.work_pos_index not in ['l', 'h', 'w', 'd', 'x']:
            self.setWindowTitle('{}{}-{}'.format(press_name, ['设定', ' setting'.upper()][self.language], self.work_pos_index))
        elif self.work_pos_index == 'l':
            self.setWindowTitle(['总压力设定', 'Total Pressure Setting'.upper()][self.language])
        elif self.work_pos_index == 'h':
            self.setWindowTitle(['测试高压设定', 'test high Pressure Setting'.upper()][self.language])
        elif self.work_pos_index == 'w':
            self.setWindowTitle(['测试低压设定', 'test low Pressure Setting'.upper()][self.language])
        elif self.work_pos_index == 'd':
            self.setWindowTitle(['密封压力设定', 'Seal Pressure Setting'.upper()][self.language])
        else:
            self.setWindowTitle(['夹具压力设定', 'Fixture Pressure Setting'.upper()][self.language])

    def setting(self):
        self.screen_rect = QApplication.desktop().screenGeometry()  # 获取显示器分辨率大小
        self.screen_height = self.screen_rect.height()
        self.screen_width = self.screen_rect.width()
        self.setGeometry((self.screen_width - self.width_) // 2, (self.screen_height - self.height_) // 2, self.width_, self.height_)
        self.setWindowModality(Qt.ApplicationModal)  # 应用程序模态，程序未完成当前对话框时，阻止和任何其他窗口进行交互
        # self.setWindowFlags(Qt.CustomizeWindowHint)  # 隐藏标题
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setFixedSize(self.width(), self.height())  # 禁止拉伸窗口大小

    def press_set_process(self):
        self.lineEdit_list = []
        self.current_lineEdit_list = []
        self.lab_press_list = []
        for i in range(2):
            self.lineEdit_list.append('self.lineEdit_press_{}'.format(i + 1))
        for i in range(3):
            self.lab_press_list.append('self.lab_press_{}'.format(i+1))
        if self.work_pos_index == 'l':  # 总压力设定
            self.lineEdit_list.append('self.lineEdit_press_3')
            self.lab_press_list.append('self.lab_press_4')
            self.lab_press1_4.setText(['预设值', 'Preset'.upper()][self.language])
            self.lab_press1_4.setStyleSheet('background-color: rgb(220, 220, 220);\n''color: rgb(255, 0, 0);')
            self.lab_press_4.setStyleSheet('background-color: rgb(220, 220, 220);\n''color: rgb(255, 0, 0);')
            self.lineEdit_press_3.setStyleSheet('background-color: rgb(250, 0, 0);\n''color: rgb(255, 255, 255);')
        for i in self.lab_press_list:
            eval(i).setText(self.unit)
        for i in self.lineEdit_list:
            eval(i).installEventFilter(self)
        """中英文切换"""
        self.lab_press_name_list = []
        text_list = [['显示值', 'Display'.upper()], ['量程上限', 'range max'.upper()], ['量程下限', 'range min'.upper()]]
        for i in range(3):
            self.lab_press_name_list.append('self.lab_press1_{}'.format(i+1))
        for i in range(3):
            eval(self.lab_press_name_list[i]).setText(text_list[i][self.language])
            eval(self.lab_press_name_list[i]).setFont(QFont('Arial', [16, 12][self.language], QFont.Bold))

    def text_process(self, text):
        text1 = text[:-4] if '.' in text else text[:-4] + '.'
        num = eval(text[-2:].lstrip('0')) - 1
        text = '0.' + num * '0' + text1[0] + text1[2:]
        return text

    def eventFilter(self, object, event):
        """给lineEdit添加单击左键事件过滤器"""
        for i in self.lineEdit_list:
            if object == eval(i):
                if event.type() == QMouseEvent.MouseButtonPress:
                    mouse_event = QMouseEvent(event)
                    if mouse_event.buttons() == Qt.LeftButton:
                        self.current_lineEdit_list.append(object)
                        text = object.text()
                        if 'e' in text:
                            if text[-3] == '-':
                                text = '-' + self.text_process(text) if text[0] == '-' else self.text_process(text)
                            else:
                                text = str(int(eval(text[:-4]) * pow(10, eval(text[-2:].lstrip('0')))))
                        self.input_num = InputNumericType(text)
                        self.input_num.show()
                        self.input_num.btn_input_ok.clicked.connect(self.press_show)
        return QWidget.eventFilter(self, object, event)

    def press_show(self):
        text = self.input_num.lineEdit_input_modify()
        current_lineEdit = self.current_lineEdit_list.pop()
        current_lineEdit.setText(text)
        self.input_num.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = PressSet('mbar', 'l', 0)
    my_show.show()
    sys.exit(app.exec_())
