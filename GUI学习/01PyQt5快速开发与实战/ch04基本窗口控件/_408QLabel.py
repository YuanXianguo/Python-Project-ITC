import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPalette

class WindowDemo(QWidget):
    def __init__(self):
        super().__init__()

        label1 = QLabel(self)
        label2 = QLabel(self)
        label3 = QLabel(self)
        label4 = QLabel(self)

        # 初始化标签控件
        label1.setText("这是一个文本标签。")
        label1.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Window, Qt.blue)
        label1.setPalette(palette)
        label1.setAlignment(Qt.AlignCenter)
        label1.setTextInteractionFlags(Qt.TextSelectableByMouse)

        label2.setText("<a href='$'>欢迎使用Python GUI应用</a>")
        # 滑过文本框绑定槽事件
        label2.linkHovered.connect(self.link_hovered)

        label3.setAlignment(Qt.AlignCenter)
        label3.setToolTip('这是一个图片标签')
        label3.setPixmap(QPixmap("pangdi.jpg"))

        label4.setText("<A href='http://www.cnblogs.com/wangshuo1/'>"
                       "欢迎访问信平的小屋</a>")
        label4.setAlignment(Qt.AlignRight)
        label4.setToolTip('这是一个超链接标签')
        # 允许label1控件访问超链接
        label4.setOpenExternalLinks(True)
        # 点击文本框绑定槽事件
        label4.linkActivated.connect(self.link_clicked)

        # 在窗口布局中添加控件
        v_box = QVBoxLayout()
        v_box.addWidget(label1)
        v_box.addStretch()
        v_box.addWidget(label2)
        v_box.addStretch()
        v_box.addWidget(label3)
        v_box.addStretch()
        v_box.addWidget(label4)

        self.setLayout(v_box)
        self.setWindowTitle("QLabel例子")

    def link_hovered(self):
        print("当鼠标滑过label-2标签时，触发事件。")

    def link_clicked(self):
        print("当用鼠标点击label-4标签时，触发事件。")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = WindowDemo()
    my_show.show()
    sys.exit(app.exec_())


