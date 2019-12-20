import sys
from PyQt5.QtWidgets import QApplication, QWidget, QCalendarWidget, QLabel
from PyQt5.QtCore import QDate
from PyQt5 import QtCore

class CalendarDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Calendar Demo")
        self.setGeometry(300, 300, 300, 300)

        self.cal = QCalendarWidget(self)
        self.cal.setMinimumDate(QDate(1990, 1, 1))
        self.cal.setMaximumDate(QDate(2100, 1, 1))
        self.cal.setGridVisible(True) # 设置日历显示网格
        self.cal.move(20, 20)
        # 从窗口组件中选定一个日期，会发射一个QtCore.QDate信号
        self.cal.clicked[QtCore.QDate].connect(self.show_date)
        date = self.cal.selectedDate() # 将所选定的日期赋给date

        self.lb = QLabel(self)
        self.lb.setText(date.toString("yyyy-MM-dd dddd"))
        self.lb.move(20, 250)

    def show_date(self, date):
        self.lb.setText(date.toString("yyyy-MM-dd dddd"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = CalendarDemo()
    my_show.show()
    sys.exit(app.exec_())
