import sys
from PyQt5.QtCore import QEvent, QTimer, Qt
from PyQt5.QtWidgets import QApplication, QMenu, QWidget
from PyQt5.QtGui import QPainter


class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Event Demo')
        self.setGeometry(300, 300, 300, 200)

        self.just_double_clicked = False
        self.key = ''
        self.text = ''
        self.message = ''

        QTimer.singleShot(3000, self.give_help)

    def give_help(self):
        self.text = '请点击这触发追踪鼠标功能'
        self.update()   # 重绘事件，也就是触发paintEvent函数

    def closeEvent(self, event):
        """重新实现关闭事件"""
        print('Closed')

    def contextMenuEvent(self, event):
        """重新实现上下文菜单事件，表示的是右键所显示的菜单事件"""
        menu = QMenu()
        one_action = menu.addAction('&One')
        one_action.triggered.connect(self.one)
        two_action = menu.addAction('&Two')
        two_action.triggered.connect(self.two)
        if not self.message:
            menu.addSeparator()
            three_action = menu.addAction('&Three')
            three_action.triggered.connect(self.three)
        menu.exec_(event.globalPos())

    """上下文菜单函数"""
    def one(self):
        self.message = 'Menu option One'
        self.update()

    def two(self):
        self.message = 'Menu option Two'
        self.update()

    def three(self):
        self.message = 'Menu option Three'
        self.update()

    def paintEvent(self, event):
        """重新实现绘制事件"""
        text = self.text
        i = text.find('\n\n')
        if i >= 0:
            text = text[0:i]
        if self.key:    # 若触发了键盘按键，则在信息文本中记录这个按键信息
            text += '\n\n你按下了：{0}'.format(self.key)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.drawText(self.rect(), Qt.AlignCenter, text)    # 绘制信息文本的内容
        if self.message:    # 若信息文本存在，则在底部居中绘制信息，5秒后清空信息文本并重绘
            painter.drawText(self.rect(), Qt.AlignBottom|Qt.AlignCenter, self.message)
            QTimer.singleShot(5000, self.clear_message)
            QTimer.singleShot(5000, self.update)

    def clear_message(self):
        """清空信息文本的槽函数"""
        self.message = ''

    def resizeEvent(self, event):
        self.text = '调整窗口的大小为：QSize({},{})'.format(event.size().width(), event.size().height())
        self.update()

    def mouseReleaseEvent(self, event):
        """重新实现鼠标释放事件"""
        # 若为双击释放，则不跟踪鼠标移动
        # 若为单击释放，则需要改变跟踪功能的状态，如果开启跟踪功能就跟踪，否则就不跟踪
        if self.just_double_clicked:
            self.just_double_clicked = False
        else:
            self.setMouseTracking(not self.hasMouseTracking())  # 单击鼠标
            if self.hasMouseTracking():
                self.text = '开启鼠标跟踪功能.\n' + '请移动一下鼠标!\n' + \
                    '单击鼠标可以关闭这个功能'
            else:
                self.text = '关闭鼠标跟踪功能.\n' + '单击鼠标可以开启这个功能'
            self.update()

    def mouseMoveEvent(self, event):
        """重新实现鼠标移动事件"""
        if not self.just_double_clicked:
            globalPos = self.mapToGlobal(event.pos())   # 将窗口坐标转换为屏幕坐标
            self.text = """鼠标位置：
            窗口坐标为：QPoint({}, {})
            屏幕坐标为：QPoint({}, {})""".format(event.pos().x(), event.pos().y(),
                                           globalPos.x(), globalPos.y())
            self.update()

    def mouseDoubleClickEvent(self, event):
        """重新实现鼠标双击事件"""
        self.just_double_clicked = True
        self.text = '你双击了鼠标'
        self.update()

    def keyPressEvent(self, event):
        """重新实现键盘按下事件"""
        self.key = ''
        if event.key() == Qt.Key_Home:
            self.key = 'Home'
        elif event.key() == Qt.Key_End:
            self.key = 'End'
        elif event.key() == Qt.Key_PageUp:
            if event.modifiers() & Qt.ControlModifier:
                self.key = 'Ctrl+PageUp'
            else:
                self.key = 'PageUp'
        elif event.key() == Qt.Key_PageDown:
            if event.modifiers() & Qt.ControlModifier:
                self.key = 'Ctrl+PageDown'
            else:
                self.key = 'PageDown'
        elif Qt.Key_A <= event.key() <= Qt.Key_Z:
            if event.modifiers() & Qt.ShiftModifier:
                self.key = 'Shift+'
            else:
                self.key += event.text()
        if self.key:
            self.key = self.key
            self.update()
        else:
            QWidget.keyPressEvent(self, event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = Widget()
    my_show.show()
    sys.exit(app.exec_())
