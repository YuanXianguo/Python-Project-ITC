import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout

class GridLayout(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建一个网格布局
        grid = QGridLayout()
        self.setLayout(grid)

        # names列表存储显示在按钮上的字符
        names = ['Cal', 'Bak', ' ', 'Close',
                '7', '8', '9', '/',
                '4', '5', '6', '*',
                '1', '2', '3', '-',
                '0', '.', '=', '+']

        # positions列表存储网格的位置的信息（元组的形式，五行四列）
        positions = [(i, j) for i in range(5) for j in range(4)]

        # zip()函数用于配对，把按钮的位置和名称按顺序组合起来，也可以理解为一个压缩过程
        for name, position in zip(names, positions):
            if name == '':
                continue
            button = QPushButton(name)
            # 可以用*解压配对的数据，*position把(i,j)解压开来
            grid.addWidget(button, *position)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Simple Calculator')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GridLayout()
    sys.exit(app.exec_())
