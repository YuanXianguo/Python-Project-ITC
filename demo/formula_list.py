import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListView
from PyQt5.QtCore import Qt, QStringListModel

from edit_formula import EditFormula
import settings


class FormulaList(QWidget):
    """配方列表"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle('配方列表')
        self.width_, self.height_ = 250, 600
        # self.setting()
        settings.get_set(self)
        self.formula_list_process()

    def formula_list_process(self):

        # 获得配方列表
        self.edit_for = EditFormula()
        self.total_formulas = self.edit_for.total_formulas

        # 创建配方列表模型
        self.formula_model = QStringListModel()
        self.formula_list = []
        for i in range(self.total_formulas):
            self.formula_list.append('配方{}：{}，{}'.format(i+1, self.edit_for.formula_name_and_steps_list[i][0],
                self.edit_for.step_template.format(self.edit_for.formula_name_and_steps_list[i][1], self.edit_for.formula_name_and_steps_list[i][2])))
        self.formula_model.setStringList(self.formula_list)

        # 创建QListView，并添加模型
        self.listView = QListView()
        self.listView.setModel(self.formula_model)
        layout = QVBoxLayout()
        layout.addWidget(self.listView)
        self.setLayout(layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = FormulaList()
    my_show.show()
    sys.exit(app.exec_())
