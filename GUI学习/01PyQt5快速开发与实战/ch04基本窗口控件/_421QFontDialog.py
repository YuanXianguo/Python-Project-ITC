import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QFontDialog

class FontDialogDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Font Dialog demo")
        self.setGeometry(300, 300, 300, 200)
        layout = QVBoxLayout()

        self.btn = QPushButton("choose font")
        self.btn.clicked.connect(self.get_font)
        layout.addWidget(self.btn)

        self.lb = QLabel("Hello,测试字体例子")
        layout.addWidget(self.lb)

        self.setLayout(layout)

    def get_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.lb.setFont(font)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = FontDialogDemo()
    my_show.show()
    sys.exit(app.exec_())
