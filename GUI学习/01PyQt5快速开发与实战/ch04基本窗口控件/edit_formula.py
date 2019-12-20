import sys, xlwt, xlrd, xlutils.copy,time
from PyQt5.QtWidgets import QApplication, QWidget, QHeaderView, QMessageBox, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt

from formula import Ui_Form  # 导入界面类
from input_numeric_type import InputNumericType  # 导入数值型键盘类
from input_name_main import InputName  # 导入名字键盘类

class EditFormula(QWidget, Ui_Form):

    """编辑配方类"""
    def __init__(self, formula_index):
        super().__init__()
        self.setupUi(self)
        self.width_, self.height_ = 1024, 768
        self.setting()
        self.formula_index = formula_index  # 获得配方索引
        self.edit_formula_process()  # 处理编辑配方的函数

    def setting(self):
        self.screen_rect = QApplication.desktop().screenGeometry()  # 获取显示器分辨率大小
        self.screen_height = self.screen_rect.height()
        self.screen_width = self.screen_rect.width()
        self.setGeometry((self.screen_width - self.width_) // 2,
                         (self.screen_height - self.height_) // 2, self.width_, self.height_)
        self.setWindowModality(Qt.ApplicationModal)  # 应用程序模态，程序未完成当前对话框时，阻止和任何其他窗口进行交互
        self.setWindowFlags(Qt.CustomizeWindowHint)  # 隐藏标题
        self.setFixedSize(self.width(), self.height())  # 禁止拉伸窗口大小

    def edit_formula_process(self):
        """处理编辑配方的函数"""
        self.total_formulas = 100  # 总配方数
        self.total_users = 2  # 只能保存2个用户
        self.current_step = 1  # 当前步
        self.edit_formula_exited = False
        self.formula_data_list = []  # 在整个系统进程中存储读取和修改后的配方详细信息
        self.formula_name_and_steps_list = []  # 在整个系统进程中存储读取和修改后的配方名称和总步数
        self.current_index_list = []  # 模拟堆栈临时存储点击的index

        self.tableView_model()  # 创建QTableView表格，并添加自定义模型
        self.get_formula()  # 读取配方信息
        self.new_step()  # 为新增步页面刷新配方信息
        self.btn_next_step.clicked.connect(self.next_step)  # 下一步
        self.btn_last_step.clicked.connect(self.last_step)  # 上一步
        self.tableView.clicked.connect(self.tableView_input)  # 单击单元格弹出数值型键盘或名字键盘
        self.btn_save_formula.clicked.connect(self.save_formula)  # 保存配方
        self.btn_exit_formula.clicked.connect(self.exit_formula)  # 退出配方

    def tableView_model(self):
        """创建QTableView表格，并添加自定义模型"""
        self.para_list = ['配方{}'.format(self.formula_index), '动作阀1', '动作阀2', '动作阀3', '动作阀4',
                          '动作阀5', '动作阀6', '伺服控制字', '伺服目标位置', '伺服扭矩(N·M)', '伺服速度(r/s)',
                          '过渡阀A', '过渡阀B', '过渡阀C', '过渡阀D', '密封', '排气', '高压(mbar)', '低压(mbar)', '流量阀(mbar)',
                          '最低压力(mbar)', '大漏值(pa)', '检测差值ΔP1(pa)', '稳压差值ΔP2(pa)']
        self.title_list = ['1:得电/2:失电', '开放时间(s)']
        self.model = QStandardItemModel(len(self.para_list), len(self.title_list))
        self.model.setHorizontalHeaderLabels(self.title_list)
        self.model.setVerticalHeaderLabels(self.para_list)
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)  # 表格填充窗口
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def get_formula(self):
        """读取配方信息并添加到存储配方信息的列表"""
        try:  # 尝试打开文件，如果打开失败就新创建一个空excel
            file = 'formula.xls'
            book = xlrd.open_workbook(file)

        except:
            book = xlwt.Workbook(encoding='utf-8')  # 创建一个Workbook对象，这就相当于创建了一个Excel文件
            book.add_sheet('formula')  # 创建一个sheet对象，一个sheet对象对应Excel文件中的一张表格
            book.save('formula.xls')
        try:  # 尝试读取配方信息，如果失败就写入默认值
            sheet = book.sheet_by_index(0)  # 通过sheet索引获得sheet对象

            """读取配方名字和步数信息"""
            formula_name_and_steps = sheet.col_values(0)
            for row in formula_name_and_steps[:self.total_formulas]:  # 读取第一列前配方总数行
                row_list = str(row).split(',')  # 以字符串形式，以逗号进行分隔
                if len(row_list) < 2:  # 如果列表长度小于2就置为默认值
                    row_list = ['新配方', '50']
                self.formula_name_and_steps_list.append(row_list)
            """读取配方详细信息"""
            column_list = sheet.col_values(self.formula_index)
            for row in column_list:
                row_list = str(row).split(',')
                if len(row_list) < 3:
                    row_list = ['0', '0', '0']
                self.formula_data_list.append(row_list)
        except:
            self.formula_name_and_steps_list.append(['新配方', '50'])
            self.formula_data_list.append(['0', '0', '0'])
        while len(self.formula_name_and_steps_list) < self.total_formulas:
            self.formula_name_and_steps_list.append(['新配方', '50'])
        while len(self.formula_name_and_steps_list) < self.total_formulas + self.total_users:
            self.formula_name_and_steps_list.append(['newuser', '123456'])
        """获得当前配方的名字和步数信息"""
        self.formula_name = self.formula_name_and_steps_list[self.formula_index-1][0]
        self.total_steps = self.formula_name_and_steps_list[self.formula_index-1][1]
        self.total_steps = eval(self.total_steps) if self.total_steps.isdigit() else 50
        while len(self.formula_data_list) < self.total_steps * len(self.para_list):
            self.formula_data_list.append(['0', '0', '0'])

    def update_show(self):
        """ 更新当前步、上一步和下一步信息"""
        self.lab_current_step.setText('第{}/{}步'.format(self.current_step, self.total_steps))
        self.btn_last_step.setEnabled(True) if self.current_step > 1 else self.btn_last_step.setEnabled(False)
        self.btn_next_step.setEnabled(
            True) if self.current_step < self.total_steps else self.btn_next_step.setEnabled(False)

    def new_step(self):
        """为新增步页面刷新配方信息"""
        self.update_show()  # 更新saved、当前步、上一步和下一步信息
        self.formula_saved = False
        """将第一行设置为配方编号、名称和步数"""
        formula_info = ['名称：{}'.format(self.formula_name), '共{}步'.format(self.total_steps)]
        for column in range(len(formula_info)):
            item = QStandardItem(formula_info[column])
            item.setTextAlignment(Qt.AlignCenter)
            item.setEditable(QAbstractItemView.NoEditTriggers)  # 设置单元格不可编辑
            self.model.setItem(0, column, item)
        for row in range(len(self.para_list)-1):
            for column in range(len(self.title_list)):
                try:
                    item = QStandardItem(str(self.formula_data_list[row + (self.current_step - 1) * len(self.para_list)][column]))
                except:  # 新增加步页面数据设置为0
                    item = QStandardItem('0')
                item.setTextAlignment(Qt.AlignCenter)
                item.setEditable(QAbstractItemView.NoEditTriggers)
                self.model.setItem(row+1, column, item)

    def next_step(self):
        """下一步"""
        self.current_step += 1
        self.new_step()

    def last_step(self):
        """上一步"""
        self.current_step -= 1
        self.new_step()

    def tableView_input(self, index):
        """根据索引显示数值型键盘或名字键盘"""
        """数值型键盘"""
        self.btn_input_list = []
        self.list = []
        for i in range(3, 11):
            self.btn_input_list.append('self.input_num.btn_input_{}'.format(i))
        if (index.row(), index.column()) not in [(0, 0)]:
            self.input_num = InputNumericType()  # 实例化数值型键盘
            self.input_num.btn_input_11.setEnabled(False)  # 将负号设置为不可选
            for i in range(len(self.para_list)):
                self.list.append((i+1, 0))
            if (index.row(), index.column()) in self.list:
                for j in range(len(self.btn_input_list)):
                    eval(self.btn_input_list[j]).setEnabled(False)  # 第一列只显示0/1/2
            else:
                for j in range(len(self.btn_input_list)):
                    eval(self.btn_input_list[j]).setEnabled(True)  # 第二列不显示负号
            self.input_num.show()
            self.input_num.lineEdit_input.clear()
            self.current_index_list.append(index)  # 临时存储点击的索引
            if (index.row(), index.column()) == (0, 1):
                self.input_num.btn_input_10.setEnabled(False)  # 将步数单元格小数点设置为不可选
            self.input_num.btn_input_ok.clicked.connect(self.tableView_show)  # 单击确定将键盘文本输出到当前index
            """名字键盘"""
        elif (index.row(), index.column()) == (0, 0):
            self.input_name = InputName()  # 实例化名字键盘
            self.input_name.show()
            self.input_name.lineEdit_input.clear()
            self.input_name.btn_input_ok.clicked.connect(self.formula_name_changed)  # 单击确定将修改配方名字

    def tableView_show(self):
        """将键盘值赋给当前点击的index"""
        index = self.current_index_list.pop()
        text1 = self.input_num.lineEdit_input.text()
        text = self.input_num.lineEdit_input_modify()
        text1 = '0' if text1 in [''] else text1
        text = text1[0] if (index.row(), index.column()) in self.list else text  # 是否得电列只显示第一个输入
        text = '共{}步'.format(text) if (index.row(), index.column()) == (0, 1) else text
        item = QStandardItem(str(text))
        item.setTextAlignment(Qt.AlignCenter)
        self.model.setItem(index.row(), index.column(), item)
        self.input_num.close()
        self.formula_saved = False

    def formula_name_changed(self):
        """将名字键盘值赋给当前点击的index(0,1)"""
        text = '名称：{}'.format(self.input_name.lineEdit_input.text())
        item = QStandardItem(str(text))
        item.setTextAlignment(Qt.AlignCenter)
        self.model.setItem(0, 0, item)
        self.input_name.close()
        self.formula_saved = False

    def save_formula(self):
        """保存配方"""
        file = 'formula.xls'
        rd_book = xlrd.open_workbook(file)
        wt_book = xlutils.copy.copy(rd_book)  # 利用xlutils.copy函数，将xlrd.Book转化为xlwt.Workbook，再用xlwt模块进行存储
        wt_sheet = wt_book.get_sheet(0)  # 通过get_sheet()获取的sheet有write()方法
        try:  # 数据改变信号使用冲突，采用遍历获取改变数据
            name = self.model.data(self.model.index(0, 0))
            steps = self.model.data(self.model.index(0, 1))
            self.formula_name_and_steps_list[self.formula_index-1][0] = name[name.index('：') + 1:]
            self.formula_name_and_steps_list[self.formula_index-1][1] = steps[steps.index('共') + 1:steps.index('步')]
            # 更新配方名称和总步数
            self.formula_name = self.formula_name_and_steps_list[self.formula_index - 1][0]
            self.total_steps = eval(self.formula_name_and_steps_list[self.formula_index - 1][1])
            for row in range(len(self.formula_name_and_steps_list)):  # 对配方信息进行更新
                column_str = '{},{}'.format(self.formula_name_and_steps_list[row][0],
                                            self.formula_name_and_steps_list[row][1])
                wt_sheet.write(row, 0, column_str)
            for row in range(len(self.para_list)-1):
                column_str = ''
                for column in range(len(self.title_list)):
                    self.formula_data_list[row + (self.current_step - 1) * len(self.para_list)][
                        column] = self.model.data(self.model.index(row + 1, column))  # 对配方列表进行更新用作装载
                    column_str += '{},'.format(self.model.data(self.model.index(row+1, column)))
                    wt_sheet.write(row + (self.current_step-1) * len(self.para_list), self.formula_index, column_str)
            wt_book.save(file)

            QMessageBox.information(self, '保存成功！', '参数保存成功！', QMessageBox.Ok)
            self.update_show()  # 更新saved、当前步、上一步和下一步信息
            self.formula_saved = True

        except:
            QMessageBox.warning(self, '保存失败！', '参数保存失败！', QMessageBox.Cancel)

    def exit_formula(self):
        """退出编辑配方"""
        if self.formula_saved:
            self.close()
            self.edit_formula_exited = True
        else:
            answer = QMessageBox.question(self, "返回主界面", "参数没有保存，确定离开?",
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if answer == QMessageBox.Yes:
                self.close()
                self.edit_formula_exited = True

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = EditFormula(1)
    my_show.show()
    sys.exit(app.exec_())


