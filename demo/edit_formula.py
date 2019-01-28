import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QHeaderView, QMessageBox, QAbstractItemView
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from formula import Ui_Form  # 导入界面类
from input_numeric_type import InputNumericType  # 导入数值型键盘类
from input_name_main import InputName  # 导入名字键盘类


class EditFormula(QWidget, Ui_Form):
    update_work_pos = pyqtSignal(int)
    """编辑配方类"""

    def __init__(self, formula_index=0):
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
        self.setGeometry((self.screen_width - self.width_) // 2, (self.screen_height - self.height_) // 2, self.width_, self.height_)
        self.setWindowModality(Qt.ApplicationModal)  # 应用程序模态，程序未完成当前对话框时，阻止和任何其他窗口进行交互
        self.setWindowFlags(Qt.CustomizeWindowHint)  # 隐藏标题
        self.setFixedSize(self.width(), self.height())  # 禁止拉伸窗口大小

    def edit_formula_process(self):
        """处理编辑配方的函数"""
        self.total_formulas = 100  # 总配方数
        self.total_formula_steps = 100  # 总步数
        self.max_digit = 13  # 配方名最长13位
        self.current_step = 1  # 当前步
        self.formula_saved = True  # 判断配方是否保存
        self.current_index_list = []  # 模拟堆栈临时存储点击的index
        self.formula_name_and_steps_list = []  # 在整个系统进程中存储读取和修改后的配方名称和总步数

        self.tableView_model()  # 创建QTableView表格，并添加自定义模型
        self.get_formula_np()  # 读取配方信息
        self.new_step()  # 为新增步页面刷新配方信息
        self.btn_next_step.clicked.connect(self.next_step)  # 下一步
        self.btn_last_step.clicked.connect(self.last_step)  # 上一步
        self.btn_current_step.clicked.connect(self.goto_step)  # 转到步
        self.tableView.clicked.connect(self.tableView_input)  # 单击单元格弹出数值型键盘或名字键盘
        self.btn_save_formula.clicked.connect(self.save_formula_np)  # 保存配方
        self.btn_exit_formula.clicked.connect(self.exit_formula)  # 退出配方

    def tableView_model(self):
        """创建QTableView表格，并添加自定义模型"""
        self.para_list = ['配方-{}'.format(self.formula_index),
                          '动作阀1', '动作阀2', '动作阀3', '动作阀4', '动作阀5', '动作阀6',
                          '伺服', '伺服转矩(N·M)', '伺服速度(r/S)', '伺服打开角度(°)',
                          '高压', '低压', '流量阀', '密封', '排气', '过渡阀A', '过渡阀B', '过渡阀C', '过渡阀D',
                          '测压ΔP1(pa)/时间(1S)', '稳压ΔP2(pa)/时间(1S)', '最低工作压力(mbar)', '大漏值(pa)']
        self.title_list = ['1:得电/2:失电', '时间(1S)']
        self.model = QStandardItemModel(len(self.para_list), len(self.title_list))
        self.model.setHorizontalHeaderLabels(self.title_list)
        self.model.setVerticalHeaderLabels(self.para_list)
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)  # 表格填充窗口
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.verticalHeader().setStretchLastSection(True)  # 表格填充窗口
        self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.model.dataChanged.connect(self.tableView_data_changed)

    def tableView_data_changed(self, index):
        """如果不是新增页面数据改变，而是用户修改数据改变才做处理"""
        if not self.newed:  # 用户修改改变数据
            changed_data = self.model.data(self.model.index(index.row(), index.column()))
            if 'e' in changed_data and 'new' not in changed_data:
                if changed_data[-3] == '-':
                    changed_data = self.text_process(changed_data)
                else:
                    changed_data = str(int(eval(changed_data[:-4]) * pow(10, eval(changed_data[-2:].lstrip('0')))))
            if '.' in changed_data:
                n = changed_data.index('.')
                changed_data = '-{}{}{}'.format(len(changed_data) - 1 - n, changed_data[:n], changed_data[n + 1:])
            if ':' in changed_data:  # 更新配方名称
                self.formula_name = changed_data[3:]
                count = 0
                for i in self.formula_name_and_steps_list:
                    print(self.formula_name, i, self.formula_name_and_steps_list.index(i), self.formula_index-1)
                    if self.formula_name in i and self.formula_name_and_steps_list.index(i) != self.formula_index-1:
                        count += 1
                        break
                if count:
                    QMessageBox.warning(self, '名字重复！', '该名字已存在，请重命名！')
                    item = QStandardItem('名称:{}'.format(self.formula_name_and_steps_list[self.formula_index - 1][0]))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setEditable(QAbstractItemView.NoEditTriggers)
                    self.model.setItem(index.row(), index.column(), item)
                else:
                    self.formula_name_and_steps_list[self.formula_index - 1][0] = self.formula_name
            elif '共' in changed_data:  # 更新配方步数
                self.total_steps = eval(changed_data[1:-1])
                self.formula_name_and_steps_list[self.formula_index - 1][1] = self.total_steps
                self.formula_data_array[self.formula_index][self.total_steps:] = 0  # 清除配方冗余数据
                self.update_show()  # 更新saved、当前步、上一步和下一步信息
            else:  # 对配方列表进行更新
                self.formula_data_array[self.formula_index][self.current_step - 1][index.row() - 1][index.column()] = changed_data

    def get_formula_np(self):
        """读取配方信息并添加到存储配方信息的4维ndarray数组"""
        self.formula_data_shape = (self.total_formulas, self.total_formula_steps, len(self.para_list) - 1, len(self.title_list))
        self.formula_name_and_steps_shape = (self.total_formula_steps * (len(self.para_list) - 1), len(self.title_list))
        self.formula_name_and_steps_shape_save = (self.total_formula_steps, len(self.para_list) - 1, len(self.title_list))
        try:  # 在整个系统进程中存储读取和修改后的配方详细信息
            self.formula_data_array = np.fromfile('formula.dat', np.int32).reshape(self.formula_data_shape)
        except:
            self.formula_data_array = np.zeros(self.formula_data_shape, np.int32)
        # 将4维数组的第0轴当前配方列另存为3维列表用于临时存储数据改变
        # self.current_formula_data_array = self.formula_data_array[self.formula_index]
        # 将4维数组保存配方名称和总步数的第0轴第0列转换为2维数组
        self.formula_name_and_steps_array = self.formula_data_array[0].reshape(self.formula_name_and_steps_shape)
        self.user_admin = self.formula_name_and_steps_array[self.total_formulas*self.max_digit][0]  # 判断是否是管理员登录
        for i in range(self.total_formulas + 2):
            name = self.num_to_alp_code(self.formula_name_and_steps_array[i * self.max_digit + 1:(i+1) * self.max_digit])
            name = 'new' if not name else name
            steps = self.formula_name_and_steps_array[i * self.max_digit][1]
            steps = 20 if not steps else steps
            self.formula_name_and_steps_list.append([name, steps])
        """获得当前配方的名字和步数信息"""
        self.formula_name = self.formula_name_and_steps_list[self.formula_index - 1][0]
        self.total_steps = self.formula_name_and_steps_list[self.formula_index - 1][1]

    def num_to_alp_code(self, array):
        """解码，将储存配方名字的数字转换为相应字母"""
        text = ''
        for i in range(len(array)):
            if array[i][0] == 61:
                text += str((array[i][1] - 86) // 21 - 90)
            elif array[i][0] == 72:
                text += str((array[i][1] - 87) // 23 - 91)
            elif array[i][0] == 83:
                text += chr((array[i][1] + 89) // 22)
            elif array[i][0] == 50:
                text += chr((array[i][1] + 88) // 24)
            else:
                break
        return text

    def alp_to_num_code(self, text):
        """numpy只保存数字"""
        """编码，将配方名字字母转换为相应ASCII码用于保存"""
        text = str(text)
        name_list = []
        for i in text:
            if i.isdigit():
                if eval(i) > 4:
                    digit = 61  # 内容标记
                    num = (eval(i) + 90) * 21 + 86
                else:
                    digit = 72
                    num = (eval(i) + 91) * 23 + 87
            else:  # 转化为ASCII码
                if ord(i) > 91:
                    digit = 83
                    num = ord(i) * 22 - 89
                else:
                    digit = 50
                    num = ord(i) * 24 - 88
            name_list.append([digit, num])
        while len(name_list) < self.max_digit - 1:
            name_list.append([0, 0])
        return name_list

    def save_formula_np(self):
        """采用numpy保存数据"""
        try:  # 更新保存用配方名称和步数列表
            index = (self.formula_index - 1) * self.max_digit
            name_list = self.alp_to_num_code(self.formula_name)
            self.formula_name_and_steps_array[index + 1:index + self.max_digit] = name_list
            self.formula_name_and_steps_array[index][1] = self.total_steps
            self.formula_data_array[0] = self.formula_name_and_steps_array.reshape(self.formula_name_and_steps_shape_save)
            # self.formula_data_array[self.formula_index] = self.current_formula_data_array
            self.formula_data_array.tofile('formula.dat', format='%d')  # 保存
            QMessageBox.information(self, '保存成功！', '参数保存成功！')
            self.formula_saved = True
        except:
            QMessageBox.warning(self, '保存失败！', '参数保存失败！')

    def update_show(self):
        """ 更新当前步、上一步和下一步信息"""
        self.btn_current_step.setText('第{}/{}步'.format(self.current_step, self.total_steps))
        self.btn_last_step.setEnabled(True) if self.current_step > 1 else self.btn_last_step.setEnabled(False)
        self.btn_next_step.setEnabled(True) if self.current_step < self.total_steps else self.btn_next_step.setEnabled(False)

    def new_step(self):
        """为新增步页面刷新配方信息"""
        self.newed = True  # 判断是否是新增页面数据改变
        self.update_show()  # 更新saved、当前步、上一步和下一步信息
        self.formula_saved = False
        """将第一行设置为配方编号、名称和步数"""
        formula_info = ['名称:{}'.format(self.formula_name), '共{}步'.format(self.total_steps)]
        for column in range(len(formula_info)):
            item = QStandardItem(formula_info[column])
            item.setTextAlignment(Qt.AlignCenter)
            item.setEditable(QAbstractItemView.NoEditTriggers)  # 设置单元格不可编辑
            self.model.setItem(0, column, item)
        for row in range(len(self.para_list)-1):
            for column in range(len(self.title_list)):
                if not self.user_admin and column == 1 and (self.para_list.index('密封') - 2 < row < self.para_list.index('过渡阀D')
                                                            or self.formula_data_array[self.formula_index][self.current_step - 1][row][0] == 2):
                    item = QStandardItem('-')
                else:
                    text = str(self.formula_data_array[self.formula_index][self.current_step - 1][row][column])
                    if '-' in text:
                        index = len(text[2:]) - eval(text[1])
                        text = text[2:][:index] + '.' + text[2:][index:]
                        if len(text) > 6:
                            text = '{:4e}'.format(eval(text))
                            text = text[:-4].rstrip('0.') + text[-4:]
                    else:
                        if len(text) > 6:
                            text = '{:5e}'.format(eval(text))
                            text = text[:-4].rstrip('0.') + text[-4:]
                    item = QStandardItem(text)
                item.setTextAlignment(Qt.AlignCenter)
                item.setEditable(QAbstractItemView.NoEditTriggers)
                self.model.setItem(row+1, column, item)
        self.newed = False

    def next_step(self):
        """下一步"""
        self.current_step += 1
        self.new_step()

    def last_step(self):
        """上一步"""
        self.current_step -= 1
        self.new_step()

    def goto_step(self):
        """跳转至目标步前处理"""
        self.input_step = InputNumericType()
        self.input_step.show()
        self.input_step.btn_input_10.setEnabled(False)  # 将小数点设置为不可选
        self.input_step.btn_input_11.setEnabled(False)  # 将负号设置为不可选
        self.input_step.lineEdit_input.clear()
        self.input_step.btn_input_ok.clicked.connect(self.goto_step_show)

    def goto_step_show(self):
        """跳转至目标步"""
        text = self.input_step.lineEdit_input_modify()
        if 1 <= eval(text) <= self.total_steps:
            self.current_step = eval(text)
            self.new_step()
            self.input_step.close()
        else:
            QMessageBox.warning(self, '输入非法！', '请输入1-{}的步数！'.format(self.total_steps))
            self.input_step.lineEdit_input.clear()

    def text_process(self, text):
        text1 = text[:-4] if '.' in text else text[:-4] + '.'
        num = eval(text[-2:].lstrip('0')) - 1
        text = '0.' + num * '0' + text1[0] + text1[2:]
        return text

    def tableView_input(self, index):
        """根据索引显示数值型键盘或名字键盘"""
        text = self.model.data(self.model.index(index.row(), index.column()))
        if 'e' in text and 'new' not in text:
            if text[-3] == '-':
                text = '-' + self.text_process(text) if text[0] == '-' else self.text_process(text)
            else:
                text = str(int(eval(text[:-4]) * pow(10, eval(text[-2:].lstrip('0')))))
        if '共' in text:
            text = text[1:-1]
        """数值型键盘"""
        self.btn_input_list = []
        self.column_list = [[], []]
        for i in range(1, len(self.para_list)):
            self.column_list[0].append((i, 0))
            self.column_list[1].append((i, 1))
        for i in range(3, 11):
            self.btn_input_list.append('self.input_num.btn_input_{}'.format(i))
        if text != '-' and (index.row(), index.column()) != (0, 0) and (index.row(), index.column()) not in self.column_list[1][-2:] \
                and (index.row(), index.column()) not in self.column_list[1][self.para_list.index('伺服'):self.para_list.index('伺服') + 3]:
            self.input_num = InputNumericType()  # 实例化数值型键盘
            self.input_num.lineEdit_input.setText(text)  # 将键盘初始内容设置为点击的lineEdit文本内容
            self.input_num.lineEdit_input.setFocus()
            self.input_num.lineEdit_input.selectAll()  # 将键盘初始内容设置为全选状态
            self.input_num.btn_input_11.setEnabled(False)  # 将负号设置为不可选
            self.input_num.show()
            if (index.row(), index.column()) in self.column_list[0][:self.para_list.index('伺服')] \
                    or (index.row(), index.column()) in self.column_list[0][self.para_list.index('高压')-1:self.para_list.index('过渡阀D')]:
                for j in range(len(self.btn_input_list)):
                    eval(self.btn_input_list[j]).setEnabled(False)  # 第一列只显示0/1/2
            else:
                for j in range(len(self.btn_input_list)):
                    eval(self.btn_input_list[j]).setEnabled(True)  # 第二列不显示负号
            self.current_index_list.append(index)  # 临时存储点击的索引
            if (index.row(), index.column()) == (0, 1):
                self.input_num.btn_input_10.setEnabled(False)  # 将步数单元格小数点设置为不可选
            self.input_num.btn_input_ok.clicked.connect(self.tableView_show)  # 单击确定将键盘文本输出到当前index
            """名字键盘"""
        elif (index.row(), index.column()) == (0, 0):
            text = text[text.index(':') + 1:]
            self.input_name = InputName()  # 实例化名字键盘
            self.input_name.lineEdit_input.setText(text)  # 将键盘初始内容设置为点击的lineEdit文本内容
            self.input_name.lineEdit_input.setFocus()
            self.input_name.lineEdit_input.selectAll()  # 将键盘初始内容设置为全选状态
            self.input_name.show()
            self.input_name.btn_input_ok.clicked.connect(self.formula_name_changed)  # 单击确定将修改配方名字

    def tableView_show(self):
        """将键盘值赋给当前点击的index"""
        index = self.current_index_list.pop()
        text = self.input_num.lineEdit_input_modify()
        if not -pow(2, 31) < eval(text) < pow(2, 31):
            QMessageBox.warning(self, '输入溢出！', '请输入-2^31-2^31之间的数字')
            text = str(self.formula_data_array[self.formula_index][self.current_step-1][index.row()-1][index.column()])
        text1 = self.input_num.lineEdit_input.text()
        text1 = '0' if text1 == '' else text1
        if (index.row(), index.column()) in self.column_list[0][:self.para_list.index('伺服')] \
                or (index.row(), index.column()) in self.column_list[0][self.para_list.index('高压')-1:self.para_list.index('过渡阀D')]:
            text = text1[0]  # 是否得电只显示第一个输入
        if (index.row(), index.column()) == (0, 1):
            if eval(text) <= self.total_formula_steps:
                text = '共{}步'.format(text)
            else:
                QMessageBox.warning(self, '修改错误！', '请修改步数不超过{}位！'.format(self.total_formula_steps))
                text = '共{}步'.format(self.formula_name_and_steps_list[self.formula_index-1][1])
        item = QStandardItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        self.model.setItem(index.row(), index.column(), item)
        self.input_num.close()
        self.formula_saved = False

    def formula_name_changed(self):
        """将名字键盘值赋给当前点击的index(0,0)"""
        text = self.input_name.lineEdit_input.text()
        text = self.formula_name if not text else text
        if len(text) < self.max_digit:
            text = '名称:{}'.format(text)
            item = QStandardItem(str(text))
            item.setTextAlignment(Qt.AlignCenter)
            self.model.setItem(0, 0, item)
            self.input_name.close()
            self.formula_saved = False
        else:
            QMessageBox.warning(self, '修改错误！', '请修改配方名不超过{}位！'.format(self.max_digit-1))

    def exit_formula(self):
        """退出编辑配方"""
        if self.formula_saved:
            self.close()
        else:
            answer = QMessageBox.question(self, "返回主界面", "参数没有保存，确定离开?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if answer == QMessageBox.Yes:
                self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        if self.formula_saved:
            self.update_work_pos.emit(self.formula_index)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = EditFormula(1)
    my_show.show()
    sys.exit(app.exec_())


