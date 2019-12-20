import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import pyqtSignal


class MySignal(QWidget):
    """通过类成员变量定义信号对象"""
    # 无参数的信号
    signal_no_parameter = pyqtSignal()
    # 带一个参数（整数）的信号
    signal_one_parameter = pyqtSignal(int)
    # 带一个参数（字符串）的信号
    signal_one_parameter_string = pyqtSignal(str)
    # 带一个参数（整数或字符串）的重载版本的信号
    signal_one_parameter_overload = pyqtSignal([int], [str])
    # 带两个参数（整数，整数）的信号
    signal_two_parameters = pyqtSignal(int, int)
    # 带两个参数（整数，字符串）的信号
    signal_two_parameters_string = pyqtSignal(int, str)
    # 带两个参数（[整数，整数]或者[整数，字符串]）的重载版本的信号
    signal_two_parameters_overload = pyqtSignal([int, int], [int, str])


class MyWidget(QWidget):
    """通过connect方法连接信号与槽函数或者可调用对象"""
    def __init__(self):
        super().__init__()
        signal = MySignal()
        # 连接无参数的信号
        signal.signal_no_parameter.connect(self.set_value_no_parameter)

        # 连接带一个参数(整数)的信号
        signal.signal_one_parameter.connect(self.set_value_one_parameter)

        # 连接带一个参数(字符串)的信号
        signal.signal_one_parameter_string.connect(self.set_value_one_parameter)

        # 连接带一个整数参数，经过重载的信号
        signal.signal_one_parameter_overload[int].connect(self.set_value_one_parameter)

        # 连接带一个字符串参数，经过重载的信号
        signal.signal_one_parameter_overload[str].connect(self.set_value_one_parameter_string)

        # 连接带两个参数（整数，整数）的信号
        signal.signal_two_parameters.connect(self.set_value_two_parameters)

        # 连接带两个参数（整数，字符串）的信号
        signal.signal_two_parameters_string.connect(self.set_value_two_parameters_string)

        # 连接带两个参数（整数，整数）的重载版本的信号
        signal.signal_two_parameters_overload[int, int].connect(self.set_value_two_parameters)

        # 连接带两个参数（整数，字符串）的重载版本的信号
        signal.signal_two_parameters_overload[int, str].connect(self.set_value_two_parameters_string)

    """定义一个槽函数，它有多个不同的输入参数"""
    def set_value_no_parameter(self):
        """无参数的槽函数"""
        pass

    def set_value_one_parameter(self, int_x):
        """带一个参数（整数）的槽函数"""
        pass

    def set_value_one_parameter_string(self, str_x):
        """带一个参数（字符串）的槽函数"""
        pass

    def set_value_two_parameters(self, int_x, int_y):
        """带两个参数（整数，整数）的槽函数"""
        pass

    def set_value_two_parameters_string(self, int_x, str_y):
        """带两个参数（整数，字符串）的槽函数"""
        pass

    def mousePressEvent(self, event):
        """通过emit方法发射信号"""

        # 发射无参数的信号
        self.signal_no_parameter.emit()

        # 发射带一个参数（整数）的信号
        self.signal_one_parameter.emit(1)

        # 发射带一个参数（字符串）的信号
        self.signal_one_parameter.emit('abc')

        # 发射带一个参数（整数）的重载版本的信号
        self.signal_one_parameter_overload[int].emit(1)

        # 发射带一个参数（字符串）的重载版本的信号
        self.signal_one_parameter_overload[str].emit('abc')

        # 发射带两个参数（整数，整数）的信号
        self.signal_two_parameters.emit(1, 2)

        # 发射带两个参数（整数，字符串）的信号
        self.signal_two_parameters_string.emit(1, 'abc')

        # 发射带两个参数（整数，整数）的信号
        self.signal_two_parameters_overload[int, int].emit(1, 2)

        # 发射带两个参数（整数，字符串）的信号
        self.signal_two_parameters_overload[int, str].emit(1, 'abc')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = MyWidget()
    my_show.show()
    sys.exit(app.exec_())
