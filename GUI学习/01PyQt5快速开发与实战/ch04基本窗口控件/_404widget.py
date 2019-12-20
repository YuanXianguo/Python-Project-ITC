import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

app = QApplication(sys.argv)
widget = QWidget()
btn = QPushButton(widget)
btn.setText("Button")
# 以QWidget左上角为（0，0）点
btn.move(20, 20)
# 若设置宽度小于规定值，则会以规定值进行显示
widget.resize(300, 200)
# 以屏幕左上角为（0，0）点
widget.move(250, 200)
widget.setWindowTitle("PyQt坐标系统例子")
widget.show()

sys.exit(app.exec_())
