import sys
from PyQt5.QtWidgets import QApplication, QWidget,  QVBoxLayout, QSlider, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class Sliderdemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Slider demo")
        self.setGeometry(300, 300, 300, 200)
        layout = QVBoxLayout()

        self.lb = QLabel("Hello PyQt5")
        self.lb.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lb)
        # 创建水平方向滑块
        self.sl = QSlider(Qt.Horizontal)
        self.sl.setMinimum(10) # 设置最小值
        self.sl.setMaximum(50) # 设置最大值
        self.sl.setSingleStep(3) # 设置步长
        self.sl.setValue(20)   # 设置当前值
        self.sl.setTickPosition(QSlider.TicksBelow)
        self.sl.setTickInterval(5)
        self.sl.valueChanged.connect(self.value_change)
        layout.addWidget(self.sl)

        self.setLayout(layout)

    def value_change(self):
        # 把滑动条的当前值设置为标签文本字体大小
        self.lb.setFont(QFont("Arial", self.sl.value()))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = Sliderdemo()
    my_show.show()
    sys.exit(app.exec_())
