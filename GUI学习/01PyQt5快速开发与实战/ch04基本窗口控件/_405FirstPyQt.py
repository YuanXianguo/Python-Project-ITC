import sys
# 在Qt5中使用的基本的GUI窗口控件都在PyQt5.QtWidgets模块中
from PyQt5.QtWidgets import QApplication, QWidget
# 每一个PyQt5程序都要有一个QApplication对象，sys.argv是一个命令行参数列表
app = QApplication(sys.argv)
# QWidget控件是所有用户界面类的父类，这里使用了没有参数的默认构造函数，
# 它没有继承其他类，我们称没有父类的控件为窗口
window = QWidget()
window.resize(300, 200)
window.move(250, 150)
window.setWindowTitle("Hello PyQt5")
window.show()
# 进入该程序的 主循环，事件处理从本行代码开始，主循环接收事件消息并将其分发给程序的各个控件
# 如果调用exit()或主控件被销毁，主循环就会结束
# 使用sys.exit()方法退出可以确保程序完整的结束
sys.exit(app.exec_())
