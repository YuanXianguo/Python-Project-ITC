import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QTextEdit, QLineEdit

class GridLayoutAndText(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        title = QLabel('Title')
        author = QLabel('Author')
        review = QLabel('Review')
        title_edit = QLineEdit()
        author_edit = QLineEdit()
        review_edit = QTextEdit()

        grid = QGridLayout()
        self.setLayout(grid)

        # 将以上6个部件进行网格布局，间距10
        grid.setSpacing(10)
        grid.addWidget(title, 1, 0)
        grid.addWidget(title_edit, 1, 1)
        grid.addWidget(author, 2, 0)
        grid.addWidget(author_edit, 2, 1)
        grid.addWidget(review, 3, 0)
        # 之前5个部件占据1个网格，reviewEdit占据了(3,1),(4,1),(5,1)共3个网格
        grid.addWidget(review_edit, 3, 1, 5, 1)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('review')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GridLayoutAndText()
    sys.exit(app.exec_())
