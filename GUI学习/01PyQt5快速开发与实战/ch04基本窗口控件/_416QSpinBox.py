import sys
from PyQt5.QtWidgets import QApplication, QWidget,  QVBoxLayout, QSpinBox, QLabel
from PyQt5.QtCore import Qt

class SpinBoxdemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SpinBox demo")
        self.setGeometry(300, 300, 300, 200)
        layout = QVBoxLayout()

        self.lb = QLabel("current value:")
        self.lb.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lb)

        self.sp = QSpinBox()
        self.sp.valueChanged.connect(self.value_change)
        layout.addWidget(self.sp)

        self.setLayout(layout)

    def value_change(self):
        # 把计数器的当前值设置到标签文本中
        self.lb.setText("current value:{}".format(str(self.sp.value())))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = SpinBoxdemo()
    my_show.show()
    sys.exit(app.exec_())
