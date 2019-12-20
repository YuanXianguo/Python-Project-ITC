import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 设置在屏幕中显示位置
        self.move(300, 300)
        # 设置窗口尺寸
        self.resize(400, 200)
        # 创建状态栏
        self.status = self.statusBar()
        # 显示5秒
        self.status.showMessage("这是状态栏提示", 5000)
        # 设置标题
        self.setWindowTitle("PyQt MainWindow 例子")
        # 设置图标
        self.setWindowIcon(QIcon("pangdi.jpg"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
