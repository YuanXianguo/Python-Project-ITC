import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent, QFont

from servo_set import Ui_ServoSet
from input_numeric_type import InputNumericType  # 导入数值型键盘类


class ServoSet(QWidget, Ui_ServoSet):
    """伺服设定"""

    def __init__(self, work_pos_index, language):
        super().__init__()
        self.setupUi(self)
        self.width_, self.height_ = 450, 350
        self.setting()
        self.work_pos_index = work_pos_index
        self.language = language
        self.setWindowTitle('{}-{}'.format(['伺服设定', 'SERVO SETTING'][self.language], self.work_pos_index))
        self.servo_set_process()

    def setting(self):
        self.screen_rect = QApplication.desktop().screenGeometry()  # 获取显示器分辨率大小
        self.screen_height = self.screen_rect.height()
        self.screen_width = self.screen_rect.width()
        self.setGeometry((self.screen_width - self.width_) // 2, (self.screen_height - self.height_) // 2, self.width_, self.height_)
        self.setWindowModality(Qt.ApplicationModal)  # 应用程序模态，程序未完成当前对话框时，阻止和任何其他窗口进行交互
        # self.setWindowFlags(Qt.CustomizeWindowHint)  # 隐藏标题
        self.setWindowFlags(Qt.WindowCloseButtonHint)  # 标题只显示关闭按钮
        self.setFixedSize(self.width(), self.height())  # 禁止拉伸窗口大小

    def servo_set_process(self):
        self.lab_list = []
        self.btn_list = []
        self.lineEdit_list = []
        self.current_lineEdit_list = []
        for i in range(6):
            if i < 5:
                self.lineEdit_list.append('self.lineEdit_servo_{}'.format(i))
                self.lab_list.append('self.lab_{}'.format(i))
            self.btn_list.append('self.btn_servo_{}'.format(i))
        for i in self.lineEdit_list:
            eval(i).installEventFilter(self)
        """中英文切换"""
        lab_text_list = [['机械齿轮', 'GEAR RATIO'], ['伺服速度', 'SERVO SPEED'], ['打开转矩', 'OPEN TORQUE'], ['关闭转矩', 'CLOSE TORQUE'], ['打开角度', 'OPEN ANGLE']]
        btn_text_list = [['伺服归零', 'servo zero'.upper()], ['伺服启动', 'servo start'.upper()], ['伺服停止', 'servo stop'.upper()],
                         ['正向点动', 'Forward'.upper()], ['反向点动', 'Reverse'.upper()], ['故障复位', 'fault reset'.upper()]]
        for i in range(len(self.lab_list)):
            eval(self.lab_list[i]).setText(lab_text_list[i][self.language])
            eval(self.lab_list[i]).setFont(QFont('Arial', [16, 12][self.language], QFont.Bold))
        for i in range(len(self.btn_list)):
            eval(self.btn_list[i]).setText(btn_text_list[i][self.language])
            eval(self.btn_list[i]).setFont(QFont('Arial', [16, 12][self.language], QFont.Bold))

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
                        if 'e' in text:  # 科学记数法
                            if text[-3] == '-':  # 小于1
                                text = '-' + self.text_process(text) if text[0] == '-' else self.text_process(text)
                            else:  # 大于1
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
    my_show = ServoSet(1,0)
    my_show.show()
    sys.exit(app.exec_())
