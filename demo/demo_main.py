import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QHeaderView, QAbstractItemView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QFont, QMouseEvent, QStandardItem

from demo import Ui_Form  # 导入主界面类
from formula_list import FormulaList  # 导入配方列表类
from edit_formula import EditFormula  # 导入编辑配方类
from servo_set_main import ServoSet  # 导入伺服设定类
from press_set_main import PressSet  # 导入压力设定类
from data_set_main import DataSet  # 导入数据设定类
from input_name_main import InputName  # 导入名字键盘类
from demo_client import AutoClient, StartTest, SysTime  # 导入通信类


class MyWindow(QWidget, Ui_Form):
    """程序主界面类"""

    def __init__(self, total_work_poses):
        super().__init__()
        self.setupUi(self)
        self.width_, self.height_ = 1024, 768
        self.setting()
        self.total_work_poses = total_work_poses
        self.chinese_english()
        self.main_process()
        self.manual_test_process()  # 处理手动测试的函数
        self.formula_process()  # 处理参数（配方）的函数
        self.auto_test_process()  # 处理自动测试的函数
        self.data_count_process()  # 处理计数统计的函数
        self.data_process()  # 处理数据处理的函数

    def setting(self):
        self.screen_rect = QApplication.desktop().screenGeometry()  # 获取显示器分辨率大小
        self.screen_height = self.screen_rect.height()
        self.screen_width = self.screen_rect.width()
        self.setGeometry((self.screen_width - self.width_) // 2, (self.screen_height - self.height_) // 2, self.width_, self.height_)
        self.setWindowModality(Qt.ApplicationModal)  # 应用程序模态，程序未完成当前对话框时，阻止和任何其他窗口进行交互
        self.setWindowFlags(Qt.CustomizeWindowHint)  # 隐藏标题
        self.setFixedSize(self.width(), self.height())  # 禁止拉伸窗口大小

    def get_sender_index(self, sender):
        """获得发送信号的工位索引"""
        if sender.objectName()[-2].isdigit():
            work_pos_index = sender.objectName()[-2:]
        else:
            work_pos_index = sender.objectName()[-1]
        work_pos_index = eval(work_pos_index) if work_pos_index.isdigit() else work_pos_index
        return work_pos_index

    def get_upper(self, lis):
        """获得大写"""
        for i in range(len(lis)):
            lis[i] = lis[i].upper()
        return lis

    def main_process(self):
        self.tabWidget_0.currentChanged.connect(self.change_tab)

    def change_tab(self, index):
        if index == 1:
            for i in self.start_test_list:
                try:
                    eval(i).running = 0
                except:
                    pass
        elif index == 2:
            for i in self.start_test_list:
                try:
                    eval(i).running = 1
                    eval(i).start()
                except:
                    pass
        # elif index == 3:
        #     self.input_name_formula = InputName()
        #     self.input_name_formula.show()
        #     self.input_name_formula.btn_input_ok.clicked.connect(self.formula_set_show)
        #     self.input_name_formula.btn_input_cancel.clicked.connect(self.formula_set_close)

    def formula_set_close(self):
        self.tabWidget_0.setCurrentIndex(0)

    def formula_set_show(self):
        text = self.input_name_formula.lineEdit_input.text()
        if text == '2':
            self.input_name_formula.close()
        else:
            QMessageBox.warning(self, '密码错误！', '请输入正确的密码！')
            self.input_name_formula.lineEdit_input.clear()

    def chinese_english(self):
        """中英切换"""
        self.language = 0  # 判断选择语言，0：汉语，1：英语
        self.btn_chinese_show.clicked.connect(self.chinese_english_show)
        self.btn_english_show.clicked.connect(self.chinese_english_show)
        self.tabWidget_list = []
        for i in range(6):
            self.tabWidget_list.append('self.tabWidget_{}'.format(i))
        self.tabWidget_chinese_text_list = [['设备信息', '手动测试', '自动测试', '参数设置', '计数统计', '数据处理'],
                                            ['手动测试1-4', '手动测试5-8', '手动测试9-12', '手动测试13-16', '手动测试17-20'],
                                            ['自动测试1-4', '自动测试5-8', '自动测试9-12', '自动测试13-16', '自动测试17-20'],
                                            ['工位1-10', '工位11-20'], ['计数1-10', '计数11-20'], ['数据导出', '工位信息']]
        self.tabWidget_english_text_list = [['Equipment\ninformation', 'manual\ntest', 'auto\ntest', 'parameter\nsetting', 'counting', 'data\nprocessing'],
                                            ['manual\ntest 1-4', 'manual\ntest 5-8', 'manual\ntest 9-12', 'manual\ntest 13-16', 'manual\ntest 17-20'],
                                            ['auto\ntest 1-4', 'auto\ntest 5-8', 'auto\ntest 9-12', 'auto\ntest 13-16', 'auto\ntest 17-20'],
                                            ['work pos 1-10', 'work pos 11-20'], ['counting 1-10', 'counting 11-20'], ['Data export', 'work pos\ninformation']]
        for i in self.tabWidget_english_text_list:
            self.get_upper(i)
        self.tabWidget_text_list = [self.tabWidget_chinese_text_list, self.tabWidget_english_text_list]
        self.equip_chinese_text_list = ['高精密气密性测试机', '宁波意德西专用设备科技有限公司', '气源压力', '测试高压', '测试低压', '密封压力', '夹具压力']
        self.equip_english_text_list = ['High Precision Air-Tightness\nTesting Machine', 'Ningbo ITC specialized Equipment Technology Co., Ltd.',
                                        'air supply\npressure', 'test high\npressure', 'test low\npressure', 'seal\npressure', 'fixture\npressure']
        self.get_upper(self.equip_english_text_list)
        self.equip_control_name_list = ['self.lab_device', 'self.lab_company', 'self.lab_gas_press', 'self.lab_high_test', 'self.lab_low_test', 'self.lab_press_sealed', 'self.lab_press_fix']
        self.equip_english_font_size = [36, 24, 22, 22, 22, 22, 22]
        self.equip_chinese_font_size = [72, 36, 28, 28, 28, 28, 28]
        self.chinese_english_list = [[self.equip_control_name_list, [self.equip_chinese_text_list, self.equip_english_text_list], [self.equip_chinese_font_size, self.equip_english_font_size]]]

    def chinese_english_show(self):
        """中英文显示"""
        self.language = 0 if self.sender() == self.btn_chinese_show else 1
        for i in range(len(self.tabWidget_text_list[self.language])):
            if i == 0:
                eval(self.tabWidget_list[i]).setFont(QFont('Arial', [20, 16][self.language], QFont.Bold))
            else:
                eval(self.tabWidget_list[i]).setFont(QFont('Arial', [18, 14][self.language], QFont.Bold))
        for i in range(6):
            for j in range(len(self.tabWidget_list)):
                try:
                    eval(self.tabWidget_list[j]).setTabText(i, self.tabWidget_text_list[self.language][j][i])
                except:
                    pass
        for tab_index in range(len(self.chinese_english_list)):
            for i in range(len(self.chinese_english_list[tab_index][0])):
                try:
                    font_size = self.chinese_english_list[tab_index][2][self.language][i]
                except:  # 设置默认字体大小
                    font_size = [14, 12][self.language]
                eval(self.chinese_english_list[tab_index][0][i]).setText(self.chinese_english_list[tab_index][1][self.language][i])
                eval(self.chinese_english_list[tab_index][0][i]).setFont(QFont('Arial', font_size, QFont.Bold))


    """手动测试配置函数"""
    def manual_test_process(self):
        """处理手动测试的函数"""
        self.btn_servo_set_list = []
        self.btn_press_set_list = []
        self.btn_manual_test_list = []
        btn_list1 = ['self.btn_out_leak_', 'self.btn_in_leak_', 'self.btn_high_press_', 'self.btn_low_press_', 'self.btn_seal_', 'self.btn_exhaust_']
        btn_list2 = []
        for i in range(1, 7):
            btn_list2.append('self.btn_action{}_'.format(i))
        btn_list3 = ['self.btn_A_', 'self.btn_B_', 'self.btn_C_', 'self.btn_D_']
        btn_list4 = ['self.btn_press_total', 'self.btn_press_high', 'self.btn_press_low', 'self.btn_press_sealed', 'self.btn_press_fix']
        for i in range(self.total_work_poses):
            self.btn_manual_test_list.append([])
        for i in range(1, self.total_work_poses + 1):
            self.btn_servo_set_list.append('self.btn_servo_set_{}'.format(i))
            self.btn_press_set_list.append('self.btn_serious_leak_{}'.format(i))
            self.btn_press_set_list.append('self.btn_min_press_{}'.format(i))
            for j in range(len(btn_list1)):
                self.btn_manual_test_list[i-1].append('{}{}'.format(btn_list1[j], i))

        self.btn_press_set_list.extend(btn_list4)

        for i in self.btn_servo_set_list:
            eval(i).clicked.connect(self.servo_set)
        for i in self.btn_press_set_list:
            eval(i).clicked.connect(self.press_set)

    def servo_set(self):
        """伺服设定"""
        work_pos_index = self.get_sender_index(self.sender())
        self.servo_setting = ServoSet(work_pos_index, self.language)
        self.servo_setting.show()

    def press_set(self):
        self.current_press_set = []
        self.current_press_set.append(self.sender())
        self.input_name = InputName()
        self.input_name.show()
        self.input_name.btn_input_ok.clicked.connect(self.press_set_check)

    def press_set_check(self):
        text = self.input_name.lineEdit_input.text()
        if text == '1':
            self.input_name.close()
            self.press_set_show()
        else:
            QMessageBox.warning(self, '密码错误！', '请输入正确的密码！')
            self.input_name.lineEdit_input.clear()

    def press_set_show(self):
        """压力设定"""
        sender = self.current_press_set.pop()
        work_pos_index = self.get_sender_index(sender)
        if 'serious' in sender.objectName():
            self.press_setting = PressSet('Pa', work_pos_index, self.language)
        else:
            self.press_setting = PressSet('mbar', work_pos_index, self.language)
        self.press_setting.show()
        self.press_setting.lab_press_show.setText(sender.text())


    """参数（配方）配置函数"""
    def formula_process(self):
        """处理参数（配方）的函数"""
        self.lab_work_pos_show_list = []  # 存储所有显示标签的列表
        self.btn_call_formula_list = []  # 存储所有调用配方按钮的列表
        self.btn_edit_formula_list = []  # 存储所有编辑配方按钮的列表
        self.btn_load_formula_list = []  # 存储所有调用配方按钮的列表
        self.lab_auto_formula_list = []  # 存储所有显示测试配方信息标签的列表
        self.get_lists()  # 获得显示标签、调用配方、编辑配方和装载配方列表
        self.current_work_pos_list = []  # 模拟堆栈临时存储当前配方
        self.current_formula_dict = {}  # 存储工位当前调用配方
        self.state_dict = {}

        for i in self.btn_call_formula_list:  # 给调用配方按钮绑定配方列表槽函数
            eval(i).clicked.connect(self.formula_list_show)
        for i in self.btn_edit_formula_list:  # 给编辑配方按钮绑定编辑界面槽函数
            eval(i).clicked.connect(self.edit_formula_show)
        for i in self.btn_load_formula_list:  # 给装载配方按钮绑定装载配符槽函数
            eval(i).clicked.connect(self.load_formula_show)

    def get_lists(self):
        """获得显示标签、调用配方、编辑配方和装载配方列表"""
        for i in range(1, self.total_work_poses + 1):
            self.lab_work_pos_show_list.append('self.lab_work_pos_show{}'.format(i))
            self.btn_call_formula_list.append('self.btn_call_formula{}'.format(i))
            self.btn_edit_formula_list.append('self.btn_edit_formula{}'.format(i))
            self.btn_load_formula_list.append('self.btn_load_formula{}'.format(i))
            self.lab_auto_formula_list.append('self.lab_auto_formula_{}'.format(i))

    def formula_list_show(self):
        """弹出配方列表"""
        sender = self.sender()
        self.current_work_pos_list.append(sender)  # 临时存储当前工位信息
        self.formula_li = FormulaList()  # 实例化配方列表
        self.formula_li.show()
        self.formula_li.listView.clicked.connect(self.formula_show)  # 给选择的配方绑定显示槽函数

    def formula_show(self, index):
        """显示已调用配方"""
        work_pos = self.current_work_pos_list.pop()
        work_pos_index = self.get_sender_index(work_pos)
        current_lab = eval(self.lab_work_pos_show_list[work_pos_index - 1])
        current_formula = self.formula_li.formula_list[index.row()]
        text = '{}'.format(current_formula[current_formula.index('：') + 1:current_formula.index('，')])
        current_lab.setText(text)  # 将当前标签显示为配方名字
        formula_index = eval(current_formula[current_formula.index('方') + 1:current_formula.index('：')])
        self.current_formula_dict[work_pos_index] = formula_index  # 将当前工位与当前调用配方组成键值对
        self.formula_li.close()

    def edit_formula_show(self):
        """弹出编辑配方窗口"""
        sender = self.sender()
        work_pos_index = self.get_sender_index(sender)
        try:
            current_formula_index = self.current_formula_dict[work_pos_index]
            self.edit_for = EditFormula(current_formula_index)  # 实例化编辑配方
            # self.edit_for.showFullScreen()  # 全屏显示
            self.edit_for.show()
            self.edit_for.update_work_pos.connect(self.update_formula_show)  # 编辑配方退出时刷新显示配方调用标签
        except:
            QMessageBox.warning(self, '操作失败！', '请先调用一个配方！')

    def update_formula_show(self, work_pos_index):
        """编辑退出后刷新显示配方调用的标签"""
        for i in self.current_formula_dict.items():
            if i[1] == work_pos_index:
                eval(self.lab_work_pos_show_list[i[0]-1]).setText('{}'.format(self.edit_for.formula_name))

    def load_formula_show(self):
        """装载配方"""
        sender = self.sender()
        work_pos_index = self.get_sender_index(sender) - 1
        try:
            formula_index = self.current_formula_dict[work_pos_index + 1]
            self.edit_for = EditFormula(formula_index)  # 实例化编辑配方
            # 装载后将配方显示为红色
            eval(self.lab_work_pos_show_list[work_pos_index]).setStyleSheet('color: rgb(255, 0, 0);\n''background-color: rgb(0, 0, 0);')

            # 设置自动测试配方显示
            eval(self.lab_auto_formula_list[work_pos_index]).setText('{}，测{}腔'.format(self.edit_for.formula_name, self.edit_for.formula_mode))
            eval(self.lab_auto_formula_list[work_pos_index]).setStyleSheet('color: rgb(255, 0, 0);\n''background-color: rgb(0, 0, 0);')

            # 实例化响应工位测试线程
            if work_pos_index == 0:
                self.auto_client_1 = AutoClient(work_pos_index, formula_index, self.edit_for.formula_steps)
                self.start_test_1 = StartTest(work_pos_index)
            elif work_pos_index == 1:
                self.auto_client_2 = AutoClient(work_pos_index, formula_index, self.edit_for.formula_steps)
                self.start_test_2 = StartTest(work_pos_index)
            elif work_pos_index == 2:
                self.auto_client_3 = AutoClient(work_pos_index, formula_index, self.edit_for.formula_steps)
                self.start_test_3 = StartTest(work_pos_index)
            elif work_pos_index == 3:
                self.auto_client_4 = AutoClient(work_pos_index, formula_index, self.edit_for.formula_steps)
                self.start_test_4 = StartTest(work_pos_index)
            elif work_pos_index == 4:
                self.auto_client_5 = AutoClient(work_pos_index, formula_index, self.edit_for.formula_steps)
                self.start_test_5 = StartTest(work_pos_index)
            elif work_pos_index == 5:
                self.auto_client_6 = AutoClient(work_pos_index, formula_index, self.edit_for.formula_steps)
                self.start_test_6 = StartTest(work_pos_index)
            elif work_pos_index == 6:
                self.auto_client_7 = AutoClient(work_pos_index, formula_index, self.edit_for.formula_steps)
                self.start_test_7 = StartTest(work_pos_index)
            elif work_pos_index == 7:
                self.auto_client_8 = AutoClient(work_pos_index, formula_index, self.edit_for.formula_steps)
                self.start_test_8 = StartTest(work_pos_index)
            elif work_pos_index == 8:
                self.auto_client_9 = AutoClient(work_pos_index, formula_index, self.edit_for.formula_steps)
                self.start_test_9 = StartTest(work_pos_index)
            elif work_pos_index == 9:
                self.auto_client_10 = AutoClient(work_pos_index, formula_index, self.edit_for.formula_steps)
                self.start_test_10 = StartTest(work_pos_index)
            elif work_pos_index == 10:
                self.auto_client_11 = AutoClient(work_pos_index, formula_index, self.edit_for.formula_steps)
                self.start_test_11 = StartTest(work_pos_index)
            elif work_pos_index == 11:
                self.auto_client_12 = AutoClient(work_pos_index, formula_index, self.edit_for.formula_steps)
                self.start_test_12 = StartTest(work_pos_index)
            elif work_pos_index == 12:
                self.auto_client_13 = AutoClient(work_pos_index, formula_index, self.edit_for.formula_steps)
                self.start_test_13 = StartTest(work_pos_index)
            elif work_pos_index == 13:
                self.auto_client_14 = AutoClient(work_pos_index, formula_index, self.edit_for.formula_steps)
                self.start_test_14 = StartTest(work_pos_index)
            elif work_pos_index == 14:
                self.auto_client_15 = AutoClient(work_pos_index, formula_index, self.edit_for.formula_steps)
                self.start_test_15 = StartTest(work_pos_index)
            elif work_pos_index == 15:
                self.auto_client_16 = AutoClient(work_pos_index, formula_index, self.edit_for.formula_steps)
                self.start_test_16 = StartTest(work_pos_index)
            elif work_pos_index == 16:
                self.auto_client_17 = AutoClient(work_pos_index, formula_index, self.edit_for.formula_steps)
                self.start_test_17 = StartTest(work_pos_index)
            elif work_pos_index == 17:
                self.auto_client_18 = AutoClient(work_pos_index, formula_index, self.edit_for.formula_steps)
                self.start_test_18 = StartTest(work_pos_index)
            elif work_pos_index == 18:
                self.auto_client_19 = AutoClient(work_pos_index, formula_index, self.edit_for.formula_steps)
                self.start_test_19 = StartTest(work_pos_index)
            elif work_pos_index == 19:
                self.auto_client_20 = AutoClient(work_pos_index, formula_index, self.edit_for.formula_steps)
                self.start_test_20 = StartTest(work_pos_index)

            eval(self.auto_client_list[work_pos_index]).data_list = self.edit_for.formula_data_array[formula_index][0:self.edit_for.formula_steps]
            eval(self.auto_client_list[work_pos_index]).client_signal.connect(self.auto_test)
            eval(self.auto_client_list[work_pos_index]).pass_count_signal.connect(self.update_pos)
            eval(self.auto_client_list[work_pos_index]).error_signal.connect(self.error_show)

            # 实例化所有启动或急停通信
            eval(self.start_test_list[work_pos_index]).start_signal.connect(self.start_test)

        except:  # 还没调用配方
            QMessageBox.warning(self, '操作失败！', '请先调用一个配方！')

    def start_test(self, work_pos_index, state):
        if work_pos_index == -1:
            for i in self.auto_client_list:
                try:
                    eval(i).running = 0
                except:
                    pass
        else:
            if state == 1:
                eval(self.auto_client_list[work_pos_index]).running = 1
                eval(self.auto_client_list[work_pos_index]).state = 1
                eval(self.auto_client_list[work_pos_index]).start()
                eval(self.lab_auto_state_list[work_pos_index]).setText('')
                self.current_test[work_pos_index][1] = 100
                for i in range(4):
                    for j in range(5):
                        if j != 4:
                            eval(self.lab_auto_abcd_list[work_pos_index][i][j+1]).setText('0')
                        else:
                            eval(self.lab_auto_abcd_list[work_pos_index][i][j+1]).setText('')
            else:
                eval(self.auto_client_list[work_pos_index]).running = 0


    """自动测试配置函数"""
    def auto_test_process(self):
        """处理自动测试的函数"""
        self.auto_client_list = []
        self.start_test_list = []
        self.lab_auto_abcd_list = []
        self.current_test = []
        for i in range(self.total_work_poses):
            self.lab_auto_abcd_list.append([[], [], [], []])
        self.lab_auto_time_list = []
        self.lab_auto_state_list = []
        self.lab_auto_min_press_list = []
        self.lab_auto_leak_list = []
        self.lab_auto_torque_list = []
        self.get_auto_list()
        self.btn_not_pass_check.clicked.connect(self.not_pass_check)

    def get_auto_list(self):
        for i in range(1, self.total_work_poses + 1):
            self.auto_client_list.append('self.auto_client_{}'.format(i))
            self.start_test_list.append('self.start_test_{}'.format(i))
            self.current_test.append([100, 100])
            for j in range(6):
                self.lab_auto_abcd_list[i-1][0].append('self.lab_auto_a{}_{}'.format(j, i))
                self.lab_auto_abcd_list[i-1][1].append('self.lab_auto_b{}_{}'.format(j, i))
                self.lab_auto_abcd_list[i-1][2].append('self.lab_auto_c{}_{}'.format(j, i))
                self.lab_auto_abcd_list[i-1][3].append('self.lab_auto_d{}_{}'.format(j, i))
            self.lab_auto_time_list.append('self.lab_auto_time_{}'.format(i))
            self.lab_auto_state_list.append('self.lab_auto_state_{}'.format(i))
            self.lab_auto_min_press_list.append('self.lab_auto_min_press_{}'.format(i))
            self.lab_auto_leak_list.append('self.lab_auto_leak_{}'.format(i))
            self.lab_auto_torque_list.append('self.lab_auto_torque_{}'.format(i))

    def auto_test(self, work_pos_index, slot):
        slot_list = slot.split(',')
        which_test = eval(slot_list[-1])
        if which_test != -1:
            self.current_test[work_pos_index][0] = self.current_test[work_pos_index][1]
            self.current_test[work_pos_index][1] = which_test
            if self.current_test[work_pos_index][0] in [0, 1, 2, 3] and self.current_test[work_pos_index][0] != self.current_test[work_pos_index][1]:
                eval(self.lab_auto_abcd_list[work_pos_index][self.current_test[work_pos_index][0]][5]).setText('合格')
            for i in range(4):
                if i == which_test:
                    for j in range(6):
                        eval(self.lab_auto_abcd_list[work_pos_index][i][j]).setStyleSheet('color: rgb(255, 0, 0);\n''background-color: rgb(0, 0, 0);')
                else:
                    for j in range(6):
                        eval(self.lab_auto_abcd_list[work_pos_index][i][j]).setStyleSheet('color: rgb(0, 0, 0);\n''background-color: rgb(220, 220, 220);')
        try:
            for i in range(4):
                if i == self.current_test[work_pos_index][1]:
                    eval(self.lab_auto_abcd_list[work_pos_index][i][1]).setText(slot_list[0])
                    eval(self.lab_auto_abcd_list[work_pos_index][i][2]).setText(slot_list[0])
                    eval(self.lab_auto_abcd_list[work_pos_index][i][3]).setText(slot_list[1])
                    eval(self.lab_auto_abcd_list[work_pos_index][i][4]).setText(self.data_count_data_list[work_pos_index+1][3])
        except:
            pass
        eval(self.lab_auto_min_press_list[work_pos_index]).setText(slot_list[2])
        eval(self.lab_auto_leak_list[work_pos_index]).setText(slot_list[3])
        eval(self.lab_auto_torque_list[work_pos_index]).setText(slot_list[4])
        eval(self.lab_auto_time_list[work_pos_index]).setText(slot_list[5])

    def error_show(self, work_pos_index, text):
        eval(self.lab_auto_state_list[work_pos_index]).setText(text)
        eval(self.lab_auto_state_list[work_pos_index]).setStyleSheet('color: rgb(255, 0, 0);\n''background-color: rgb(0, 0, 0);')
        try:
            if text == '合格':
                eval(self.lab_auto_abcd_list[work_pos_index][self.current_test[work_pos_index][1]][5]).setText('合格')
            else:
                eval(self.lab_auto_abcd_list[work_pos_index][self.current_test[work_pos_index][1]][5]).setText('不合格')
        except:
            pass

        # 保存测试结果
        # self.para_list = ['系统时间', '班次', '配方', '测试模式', '测试时间', '测试结果', 'A-ΔP1', 'A-ΔP2', 'A-全开扭矩', 'A-全关扭矩', 'A-测试结果',
        #                   'B-ΔP1', 'B-ΔP2', 'B-全开扭矩', 'B-全关扭矩', 'B-测试结果', 'C-ΔP1', 'C-ΔP2', 'C-全开扭矩', 'C-全关扭矩', 'C-测试结果',
        #                   'D-ΔP1', 'D-ΔP2', 'D-全开扭矩', 'D-全关扭矩', 'D-测试结果', '合格数', '不合格数', '总数', '合格率']
        text_list = eval(self.lab_auto_formula_list[work_pos_index]).text().split('，')
        current_list = [self.lab_data_time.text(), self.lineEdit_0.text(), text_list[0], text_list[1], eval(self.lab_auto_time_list[work_pos_index]).text(),
                        eval(self.lab_auto_state_list[work_pos_index]).text()]
        for i in range(4):
            for j in range(5):
                current_list.append(eval(self.lab_auto_abcd_list[work_pos_index][i][j+1]).text())
        for i in range(4):
            current_list.append(str(self.data_count_data_list[work_pos_index+1][i]))
        self.test_result_list[work_pos_index].append(current_list)
        print(self.test_result_list)

    def not_pass_check(self):
        if self.btn_not_pass_check.isChecked():
            self.btn_not_pass_check.setText('不合格品箱检测')
        else:
            self.btn_not_pass_check.setText('不合格品箱不检测')


    """计数统计配置函数"""
    def data_count_process(self):
        """处理计数统计的函数"""
        self.data_count_data_list = []
        self.lab_count_qualify_list = []
        self.lab_count_not_qualify_list = []
        self.lab_count_total_list = []
        self.lab_count_pass_rate_list = []
        self.btn_count_clear_list = []
        self.lab_count_list = [self.lab_count_qualify_list, self.lab_count_not_qualify_list, self.lab_count_total_list, self.lab_count_pass_rate_list]
        self.get_data_count_list()  # 获得计数统计页面所有的控件列表
        for i in range(len(self.btn_count_clear_list)):
            eval(self.btn_count_clear_list[i]).clicked.connect(self.data_count_clear)

    def get_data_count_list(self):
        """获得计数统计页面所有的控件列表"""
        for i in range(self.total_work_poses + 1):
            self.data_count_data_list.append([0, 0, 0, 0])
            self.lab_count_qualify_list.append('self.lab_count_qualify_{}'.format(i))
            self.lab_count_not_qualify_list.append('self.lab_count_not_qualify_{}'.format(i))
            self.lab_count_total_list.append('self.lab_count_total_{}'.format(i))
            self.lab_count_pass_rate_list.append('self.lab_count_pass_rate_{}'.format(i))
            self.btn_count_clear_list.append('self.btn_count_clear_{}'.format(i))
        # 总计数2
        self.data_count_data_list.append([0, 0, 0, 0])
        self.lab_count_qualify_list.append('self.lab_count_qualify_{}'.format(21))
        self.lab_count_not_qualify_list.append('self.lab_count_not_qualify_{}'.format(21))
        self.lab_count_total_list.append('self.lab_count_total_{}'.format(21))
        self.lab_count_pass_rate_list.append('self.lab_count_pass_rate_{}'.format(21))
        self.btn_count_clear_list.append('self.btn_count_clear_{}'.format(21))

    def data_count_clear(self):
        """清除计数统计"""
        sender = self.sender()
        work_pos_index = self.get_sender_index(sender)
        if work_pos_index in [0, 21]:  # 如果点击的是总清零就将所有数据清空
            for i in range(self.total_work_poses + 2):
                for j in range(2):
                    self.data_count_data_list[i][j] = 0
                self.update_data_count(i)
        else:
            for i in range(2):  # 将总计数减掉清除的工位计数并将相应计数标签清除
                self.data_count_data_list[0][i] -= self.data_count_data_list[i][i]
                self.data_count_data_list[-1][i] -= self.data_count_data_list[i][i]
                self.data_count_data_list[i][i] = 0
            update_list = [work_pos_index, 0, -1]
            for i in update_list:
                self.update_data_count(i)

    def update_pos(self, work_pos_index, j):
        """计数器"""
        update_list = [work_pos_index, 0, -1]
        for work_pos_index_ in update_list:
            self.data_count_data_list[work_pos_index_][j] += 1
            self.update_data_count(work_pos_index_)

    def update_data_count(self, i):
        """对修改的标签进行更新"""
        self.data_count_data_list[i][2] = self.data_count_data_list[i][0] + self.data_count_data_list[i][1]
        self.data_count_data_list[i][3] = '{:.2f}%'.format(self.data_count_data_list[i][0] / self.data_count_data_list[i][2] * 100) \
            if self.data_count_data_list[i][2] != 0 else '{:.2f}%'.format(0)
        # for i in range(self.total_work_poses + 2):  # 将计数标签显示相应结果
        for j in range(4):
            eval(self.lab_count_list[j][i]).setText(str(self.data_count_data_list[i][j]))


    """数据处理配置函数"""
    def data_process(self):
        """处理数据配置的函数"""
        self.sys_time = SysTime()
        self.sys_time.start()
        self.sys_time.sys_time_signal.connect(self.sys_time_show)
        self.btn_start_list = []
        self.tableView_model()  # 创建QTableView表格，并添加自定义模型
        self.btn_data_process_list = []  # 存储所有工位的列表
        self.test_result_list = []  # 储存测试结果
        self.get_data_process_list()  # 获得列表
        for i in self.btn_data_process_list:  # 给工位绑定槽函数
            eval(i).clicked.connect(self.data_process_show)
        self.btn_data_process_set.clicked.connect(self.data_set_show)  # 点击设置弹出设置界面

    def get_data_process_list(self):
        for i in range(1, self.total_work_poses + 1):  # 获得工位列表
            self.btn_start_list.append(1)
            self.btn_data_process_list.append('self.btn_data_process_{}'.format(i))
            self.test_result_list.append([])

    def sys_time_show(self, time):
        self.lab_data_time.setText(time)

    def tableView_model(self):
        """创建QTableView表格，并添加自定义模型"""
        self.para_list = ['系统时间', '班次', '配方', '测试模式', '测试时间', '测试结果',
                          'A-ΔP1', 'A-ΔP2', 'A-全开扭矩', 'A-全关扭矩', 'A-测试结果', 'B-ΔP1', 'B-ΔP2', 'B-全开扭矩', 'B-全关扭矩', 'B-测试结果',
                          'C-ΔP1', 'C-ΔP2', 'C-全开扭矩', 'C-全关扭矩', 'C-测试结果', 'D-ΔP1', 'D-ΔP2', 'D-全开扭矩', 'D-全关扭矩', 'D-测试结果',
                          '合格数', '不合格数', '总数', '合格率']
        for i in range(len(self.para_list)):  # 用中文空白字符填充使结果对齐，并根据内容自动调整行宽
            self.para_list[i] = '{0:{1:}^8}'.format(self.para_list[i], chr(12288))

        self.row_list = []
        for i in range(20):
            self.row_list.append('第{}行'.format(i + 1))
        self.model = QStandardItemModel(len(self.row_list), len(self.para_list))
        self.model.setHorizontalHeaderLabels(self.para_list)
        self.model.setVerticalHeaderLabels(self.row_list)
        self.tableView.setModel(self.model)
        self.tableView.verticalHeader().setStretchLastSection(True)  # 表格填充窗口
        self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def set_new_item(self, row, column, text):
        """设置单元格"""
        item = QStandardItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        item.setEditable(QAbstractItemView.NoEditTriggers)  # 设置单元格不可编辑
        self.model.setItem(row, column, item)

    def data_process_show(self):
        sender = self.sender()
        work_pos_index = self.get_sender_index(sender) - 1
        sender.setStyleSheet('background-color: rgb(255, 0, 0);\n''color: rgb(255, 255, 255);')
        for i in self.btn_data_process_list:
            if i != self.btn_data_process_list[work_pos_index]:
                eval(i).setStyleSheet('background-color: rgb(220, 220, 220);\n''color: rgb(0, 0, 0);')

        if self.btn_start_list[work_pos_index]:
            self.btn_start_list[work_pos_index] = 0
            try:
                eval(self.start_test_list[work_pos_index]).start_signal_list[work_pos_index][0] = 1
            except:
                pass
        else:
            self.btn_start_list[work_pos_index] = 1
            try:
                eval(self.start_test_list[work_pos_index]).start_signal_list[work_pos_index][1] = 1
            except:
                pass

        for row in range(len(self.row_list)):
            for column in range(len(self.para_list)):
                try:
                    text = str(self.test_result_list[work_pos_index][row][column])
                    print(text)
                except:
                    text = ''
                self.set_new_item(row, column, text)

    def data_set_show(self):
        self.setting = DataSet()
        self.setting.show()

    def eventFilter(self, object, event):
        """给lineEdit添加单击左键事件过滤器"""
        if object == self.lineEdit_input:
            if event.type() == QMouseEvent.MouseButtonPress:
                mouse_event = QMouseEvent(event)
                if mouse_event.buttons() == Qt.LeftButton:
                    self.has_selected = 0
        return QWidget.eventFilter(self, object, event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = MyWindow(4)
    # my_show.showFullScreen()  # 全屏显示
    my_show.show()
    sys.exit(app.exec_())
