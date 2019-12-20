import sys, math
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter

class DrawingPointDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("在窗口中绘制一个个点")
        self.setGeometry(300, 300, 300, 200)

    def paintEvent(self, event):
        """重构paintEvent函数"""
        painter = QPainter(self)
        painter.begin(self)
        self.draw_points(painter)
        painter.end()

    def draw_points(self, qp):
        qp.setPen(Qt.red)
        # 每次调整窗口大小时，都会生成一个绘图事件，使用size()获得窗口的当前大小
        size = self.size()

        for i in range(1000):
            # 绘制正弦函数图形，它的周期是[-100,100]
            x = 100 * (-1+2.0*i/1000) + size.width()/2.0
            y = -50 * math.sin((x-size.width()/2.0)*math.pi/50) + size.height()/2.0
            # 使用drawPoint()方法绘制一个个点
            qp.drawPoint(x, y)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = DrawingPointDemo()
    my_show.show()
    sys.exit(app.exec_())
