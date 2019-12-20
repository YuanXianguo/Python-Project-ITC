import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QFont

class DrawingDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("在窗口中绘制文字")
        self.setGeometry(300, 300, 300, 200)
        self.text = "欢迎学习PyQt5"

    def paintEvent(self, event):
        """重构paintEvent函数"""
        # 初始化绘图工具
        painter = QPainter(self)
        # 开始在窗口中绘制
        painter.begin(self)
        # 自定义绘制方法
        self.draw_text(event, painter)
        # 结束在窗口中绘制
        painter.end()

    def draw_text(self, event, qp):
        # 设置画笔的颜色
        qp.setPen(QColor(168, 34, 3))
        # 设置字体
        qp.setFont(QFont('SimSun', 20))
        # 绘制文字
        qp.drawText(event.rect(), Qt.AlignCenter, self.text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = DrawingDemo()
    my_show.show()
    sys.exit(app.exec_())
