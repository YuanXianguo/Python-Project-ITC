import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel, QScrollBar
from PyQt5.QtGui import QPalette, QFont, QColor


class ScrollBarDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("ScrollBar Demo")
        self.setGeometry(300, 300, 300, 200)
        layout = QHBoxLayout()

        self.lb = QLabel('拖动滑块改变颜色')
        self.lb.setFont(QFont('Arial', 16))
        layout.addWidget(self.lb)

        self.s1 = QScrollBar()
        self.s1.setMaximum(255)
        self.s1.sliderMoved.connect(self.sliderval)
        layout.addWidget(self.s1)

        self.s2 = QScrollBar()
        self.s2.setMaximum(255)
        self.s2.sliderMoved.connect(self.sliderval)
        layout.addWidget(self.s2)

        self.s3 = QScrollBar()
        self.s3.setMaximum(255)
        self.s3.sliderMoved.connect(self.sliderval)
        layout.addWidget(self.s3)

        self.setLayout(layout)

    def sliderval(self):
        color = QColor(self.s1.value(), self.s2.value(), self.s3.value())
        palette = QPalette()
        palette.setColor(QPalette.Foreground, color)
        self.lb.setPalette(palette)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = ScrollBarDemo()
    my_show.show()
    sys.exit(app.exec_())
