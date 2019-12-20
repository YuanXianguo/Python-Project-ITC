# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '_002main.py'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

import sys,socket
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget
from _002test import Ui_Form

class Mywindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.MAX_BYTES = 65535
        self.thatIP = '127.0.0.1'
        self.that_port = 1060
        self.text = self.lineEdit.text()
        #self.pushButton.clicked.connect(self.client)
        self.pushButton.clicked.connect(self.pr)
    def pr(self):
        print(self.text)

    def client(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sen_text = 'The time is {}'.format(datetime.now())
        sen_data = sen_text.encode('ascii')
        sock.sendto(sen_data, (self.thatIP, self.that_port))
        print('The OS assigned me the address {}'.format(sock.getsockname()))
        rec_data, address = sock.recvfrom(self.MAX_BYTES)
        rec_text = rec_data.decode('ascii')
        print('The server {} replied {!r}'.format(address, rec_text))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = Mywindow()
    my_show.show()
    sys.exit(app.exec_())
