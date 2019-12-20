import sys, socket
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow
from _001简单通信 import Ui_MainWindow

class MyForm(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 设置客户端
        self.MAX_BYTES = 65535

        self.connectButton.clicked.connect(self.client2)

        # 窗口多开
        self.anotherButton.clicked.connect(self.another_window)

    def another_window(self):
        self.another = MyForm()
        self.another.show()

    def client(self):
        self.that_textEdit.setPlainText('网络连接中')
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sen_text = 'The time is {}'.format(datetime.now())
        self.this_textEdit.setPlainText(sen_text)
        sen_data = sen_text.encode('ascii')
        sock.sendto(sen_data, (self.that_lineEdit.text(), eval(self.that_lineEdit2.text())))
        self.that_textEdit.setPlainText('The OS assigned me the address {}'.format(sock.getsockname()))
        print('The OS assigned me the address {}'.format(sock.getsockname()))
        rec_data, address = sock.recvfrom(self.MAX_BYTES)
        rec_text = rec_data.decode('ascii')
        self.that_textEdit.setPlainText('The server {} replied {!r}'.format(address, rec_text))
        print('The server {} replied {!r}'.format(address, rec_text))

    def client2(self):
        self.that_textEdit.setPlainText('网络连接中')
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sen_text = '当前时间 {}'.format(datetime.now())
        self.this_textEdit.setPlainText(sen_text)
        sen_data = sen_text.encode('utf-8')
        sock.sendto(sen_data, (self.that_lineEdit.text(), eval(self.that_lineEdit2.text())))
        self.that_textEdit.setPlainText('系统给我分配了地址{}'.format(sock.getsockname()))
        print('The OS assigned me the address {}'.format(sock.getsockname()))
        rec_data, address = sock.recvfrom(self.MAX_BYTES)
        rec_text = rec_data.decode('utf-8')
        self.that_textEdit.setPlainText('服务器 {} 回复 {!r}'.format(address, rec_text))
        print('The server {} replied {!r}'.format(address, rec_text))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_form = MyForm()
    my_form.show()
    sys.exit(app.exec_())

