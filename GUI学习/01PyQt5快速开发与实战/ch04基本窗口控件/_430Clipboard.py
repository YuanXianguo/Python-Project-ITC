import sys, os
from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QMimeData

class ClipboardDemo(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clipboard Demo")
        text_copy_btn = QPushButton('&Copy Text')
        text_paste_btn = QPushButton('Paste &Text')
        html_copy_btn = QPushButton('C&opy HTML')
        html_paste_btn = QPushButton('Paste &HTML')
        image_copy_btn = QPushButton('Co&py Image')
        image_paste_btn = QPushButton('Paste &Image')
        self.text_label = QLabel('Qriginal text')
        self.image_label = QLabel()
        self.image_label.setPixmap(QPixmap(os.path.join(os.path.dirname(__file__), 'pangdi02.jpg')))

        layout = QGridLayout()
        layout.addWidget(text_copy_btn, 0, 0)
        layout.addWidget(text_paste_btn, 1, 0)
        layout.addWidget(image_copy_btn, 0, 1)
        layout.addWidget(image_paste_btn, 1, 1)
        layout.addWidget(html_copy_btn, 0, 2)
        layout.addWidget(html_paste_btn, 1, 2)
        layout.addWidget(self.text_label, 2, 0, 1, 2)
        layout.addWidget(self.image_label, 2, 2)
        self.setLayout(layout)
        text_copy_btn.clicked.connect(self.copy_text)
        text_paste_btn.clicked.connect(self.paste_text)
        html_copy_btn.clicked.connect(self.copy_html)
        html_paste_btn.clicked.connect(self.paste_html)
        image_copy_btn.clicked.connect(self.copy_image)
        image_paste_btn.clicked.connect(self.paste_image)

    def copy_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText("I've been clipboard!")

    def paste_text(self):
        clipboard = QApplication.clipboard()
        self.text_label.setText(clipboard.text())

    def copy_image(self):
        clipboard = QApplication.clipboard()
        clipboard.setPixmap(QPixmap(os.path.join(os.path.dirname(__file__), 'pangdi.jpg')))

    def paste_image(self):
        clipboard = QApplication.clipboard()
        self.image_label.setPixmap(clipboard.pixmap())

    def copy_html(self):
        mime_data = QMimeData()
        mime_data.setHtml('<b>Bold and <font color=red>Red</font></b>')
        clipboard = QApplication.clipboard()
        clipboard.setMimeData(mime_data)

    def paste_html(self):
        clipboard = QApplication.clipboard()
        mime_data = clipboard.mimeData()
        if mime_data.hasHtml():
            self.text_label.setText(mime_data.html())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = ClipboardDemo()
    my_show.show()
    sys.exit(app.exec_())
