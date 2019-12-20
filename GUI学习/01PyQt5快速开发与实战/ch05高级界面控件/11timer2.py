import sys
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import Qt, QTimer
def test():
    print(1)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    label = QLabel('<font color=red size=128><b>'
                   'Hello PyQt，窗口会在3秒后消失！</b></font>')
    # 无边框窗口
    label.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
    label.show()

    # 设置10秒后自动退出
    QTimer.singleShot(3000, test)
    sys.exit(app.exec_())


