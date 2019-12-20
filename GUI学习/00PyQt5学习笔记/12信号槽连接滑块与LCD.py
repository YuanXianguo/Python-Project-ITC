import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLCDNumber, QSlider
from PyQt5.QtCore import Qt

class QSliderQLCD(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建滑块和LCD部件
        lcd = QLCDNumber(self)
        slider = QSlider(Qt.Horizontal, self)

        # 设置布局
        v_box = QVBoxLayout()
        v_box.addWidget(lcd)
        v_box.addWidget(slider)
        self.setLayout(v_box)

        slider.valueChanged.connect(lcd.display)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('signals-slots')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QSliderQLCD()
    sys.exit(app.exec_())
