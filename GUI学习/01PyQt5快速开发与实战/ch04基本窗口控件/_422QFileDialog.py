import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QTextEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QDir

class FileDialogDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Dialog demo")
        self.setGeometry(300, 300, 300, 200)
        layout = QVBoxLayout()

        self.btn1 = QPushButton("加载图片")
        self.btn1.clicked.connect(self.get_file)
        layout.addWidget(self.btn1)

        self.lb = QLabel("此处加载图片")
        layout.addWidget(self.lb)

        self.btn2 = QPushButton("加载文本文件")
        self.btn2.clicked.connect(self.get_files)
        layout.addWidget(self.btn2)

        self.te = QTextEdit()
        layout.addWidget(self.te)

        self.setLayout(layout)

    def get_file(self):
        f_name, _ = QFileDialog.getOpenFileName(self, "Open file",
                               "C:\\", "Image files (*.jpg *.gif)")
        self.lb.setPixmap(QPixmap(f_name))

    def get_files(self):
        file = QFileDialog()
        file.setFileMode(QFileDialog.AnyFile)
        file.setFilter(QDir.Files)
        if file.exec_():
            file_names = file.selectedFiles()
            with open(file_names[0], 'r') as f:
                data = f.read()
                self.te.setText(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = FileDialogDemo()
    my_show.show()
    sys.exit(app.exec_())
