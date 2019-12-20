import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGroupBox, QCheckBox, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt

class CheckBoxdemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CheckBox demo")
        self.setGeometry(300, 300, 300, 200)
        layout = QHBoxLayout()
        group_box = QGroupBox("Checkboxes")
        group_box.setFlat(False)

        self.check_box1 = QCheckBox("&Checkbox1")
        self.check_box1.setChecked(True)
        self.check_box1.stateChanged.connect(lambda: self.btn_state(self.check_box1))
        layout.addWidget(self.check_box1)

        self.check_box2 = QCheckBox("Checkbox2")
        self.check_box2.setCheckState(Qt.Unchecked)
        self.check_box2.toggled.connect(lambda: self.btn_state(self.check_box2))
        layout.addWidget(self.check_box2)

        self.check_box3 = QCheckBox("Checkbox3")
        self.check_box3.setTristate(True) # 设置为三态复选框
        self.check_box3.setCheckState(Qt.PartiallyChecked) # 组件被半选中
        self.check_box3.stateChanged.connect(lambda: self.btn_state1(self.check_box3))
        layout.addWidget(self.check_box3)

        group_box.setLayout(layout)
        main_layout = QVBoxLayout()
        main_layout.addWidget(group_box)
        self.setLayout(main_layout)

    def btn_state(self, btn):
        if btn.isChecked():
            print(btn.text() + " is selected")
        else:
            print(btn.text() + " is deselected")
    def btn_state1(self, btn):
        print(btn.checkState())
if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = CheckBoxdemo()
    my_show.show()
    sys.exit(app.exec_())
