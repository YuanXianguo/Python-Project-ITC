import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QFormLayout

class LineEditDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QLineEdit例子")

        # 初始化
        layout = QFormLayout()
        normal_line_edit = QLineEdit()
        no_echo_line_edit = QLineEdit()
        password_line_edit = QLineEdit()
        password_echo_on_edit_line_edit = QLineEdit()
        # 设置文本框浮显文字
        normal_line_edit.setPlaceholderText('Normal')
        no_echo_line_edit.setPlaceholderText('NoEcho')
        password_line_edit.setPlaceholderText('Password')
        password_echo_on_edit_line_edit.setPlaceholderText('PasswordEchoOnEdit')
        # 设置文本框显示格式
        normal_line_edit.setEchoMode(QLineEdit.Normal)
        no_echo_line_edit.setEchoMode(QLineEdit.NoEcho)
        password_line_edit.setEchoMode(QLineEdit.Password)
        password_echo_on_edit_line_edit.setEchoMode(QLineEdit.PasswordEchoOnEdit)

        # 设置布局
        layout.addRow('Normal', normal_line_edit)
        layout.addRow('NoEcho', no_echo_line_edit)
        layout.addRow('Password', password_line_edit)
        layout.addRow('PasswordEchoOnEdit', password_echo_on_edit_line_edit)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = LineEditDemo()
    my_show.show()
    sys.exit(app.exec_())
