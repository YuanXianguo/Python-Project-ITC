import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QHeaderView
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtGui import QMouseEvent, QStandardItemModel, QFont

from demo import Ui_Form  # 导入主界面类
from formula_list import FormulaList  # 导入配方列表类
from edit_formula import EditFormula  # 导入编辑配方类
from servo_set_main import ServoSet  # 导入伺服设定类
from press_set_main import PressSet  # 导入压力设定类
from data_set_main import DataSet  # 导入数据设定类


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

    def main_process(self):
        self.tabWidget_0.currentChanged.connect(self.change_tab)

    def change_tab(self, index):
        if index == 1:
            for i in self.auto_client_list:
                try:
                    eval(i).running = 0
                except:
                    pass
        elif index == 2:
            for i in self.auto_client_list:
                try:
                    eval(i).running = 1
                    eval(i).start()
                except:
                    pass

    def chinese_english(self):
        """中英切换"""
        self.language = 0  # 判断选择语言，0：汉语，1：英语
        self.btn_chinese_show.clicked.connect(self.chinese_show)
        self.btn_english_show.clicked.connect(self.english_show)
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

        self.chinese_text_list = ['高精密气密性测试机', '宁波意德西专用设备科技有限公司', '气源压力', '测试高压', '测试低压', '气源报警']
        self.english_text_list = ['High Precision Air-Tightness\nTesting Machine', 'Ningbo ITC specialized Equipment Technology Co., Ltd.',
                                  'air supply\npressure', 'test high\npressure', 'test low\npressure', 'air judge\npressure']
        self.control_name_list = ['self.lab_device', 'self.lab_company', 'self.lab_gas_press', 'self.lab_high_test', 'self.lab_low_test', 'self.lab_gas_warn']
        self.english_font_size = [36, 24, 22, 22, 22, 22]
        self.chinese_font_size = [72, 36, 28, 28, 28, 28]

    def chinese_show(self):
        """中文显示"""
        self.language = 0
        for i in range(len(self.tabWidget_chinese_text_list)):
            if i == 0:
                eval(self.tabWidget_list[i]).setFont(QFont('Arial', 20, QFont.Bold))
            else:
                eval(self.tabWidget_list[i]).setFont(QFont('Arial', 18, QFont.Bold))
        for i in range(6):
            eval(self.tabWidget_list[0]).setTabText(i, self.tabWidget_chinese_text_list[0][i])
        for i in range(5):
            eval(self.tabWidget_list[1]).setTabText(i, self.tabWidget_chinese_text_list[1][i])
            eval(self.tabWidget_list[2]).setTabText(i, self.tabWidget_chinese_text_list[2][i])
        for i in range(2):
            eval(self.tabWidget_list[3]).setTabText(i, self.tabWidget_chinese_text_list[3][i])
            eval(self.tabWidget_list[4]).setTabText(i, self.tabWidget_chinese_text_list[4][i])
            eval(self.tabWidget_list[5]).setTabText(i, self.tabWidget_chinese_text_list[5][i])

        for i in range(len(self.control_name_list)):
            eval(self.control_name_list[i]).setText(self.chinese_text_list[i])
            eval(self.control_name_list[i]).setFont(QFont('Arial', self.chinese_font_size[i], QFont.Bold))

    def english_show(self):
        """英文显示"""
        self.language = 1
        for i in range(len(self.tabWidget_chinese_text_list)):
            if i == 0:
                eval(self.tabWidget_list[i]).setFont(QFont('Arial', 16, QFont.Bold))
            else:
                eval(self.tabWidget_list[i]).setFont(QFont('Arial', 14, QFont.Bold))
        for i in range(6):
            eval(self.tabWidget_list[0]).setTabText(i, self.tabWidget_english_text_list[0][i].upper())
        for i in range(5):
            eval(self.tabWidget_list[1]).setTabText(i, self.tabWidget_english_text_list[1][i].upper())
            eval(self.tabWidget_list[2]).setTabText(i, self.tabWidget_english_text_list[2][i].upper())
        for i in range(2):
            eval(self.tabWidget_list[3]).setTabText(i, self.tabWidget_english_text_list[3][i].upper())
            eval(self.tabWidget_list[4]).setTabText(i, self.tabWidget_english_text_list[4][i].upper())
            eval(self.tabWidget_list[5]).setTabText(i, self.tabWidget_english_text_list[5][i].upper())
        for i in range(len(self.control_name_list)):
            eval(self.control_name_list[i]).setText(self.english_text_list[i].upper())
            eval(self.control_name_list[i]).setFont(QFont('Arial', self.english_font_size[i], QFont.Bold))


    """手动测试配置函数"""
    def manual_test_process(self):
        """处理手动测试的函数"""
        self.btn_servo_set_list = []
        self.btn_press_set_list = []
        for i in range(4):
            self.btn_servo_set_list.append('self.btn_servo_set_{}'.format(i+1))
            self.btn_press_set_list.append('self.btn_serious_leak_{}'.format(i + 1))
            self.btn_press_set_list.append('self.btn_min_press_{}'.format(i + 1))
        self.btn_press_set_list.append('self.btn_press_total')
        self.btn_press_set_list.append('self.btn_press_high')
        self.btn_press_set_list.append('self.btn_press_low')
        for i in self.btn_servo_set_list:
            eval(i).clicked.connect(self.servo_set)
        for i in self.btn_press_set_list:
            eval(i).clicked.connect(self.press_set)

    def servo_set(self):
        """伺服设定"""
        sender = self.sender()
        if sender.objectName()[-2].isdigit():
            work_pos_index = sender.objectName()[-2:]
        else:
            work_pos_index = sender.objectName()[-1]
        self.servo_setting = ServoSet(work_pos_index, self.language)
        self.servo_setting.show()

    def press_set(self):
        """压力设定"""
        sender = self.sender()
        if sender.objectName()[-2].isdigit():
            work_pos_index = sender.objectName()[-2:]
        else:
            work_pos_index = sender.objectName()[-1]
        if 'serious' in sender.objectName():
            self.press_setting = PressSet('Pa', work_pos_index, self.language)
        else:
            self.press_setting = PressSet('mbar', work_pos_index, self.language)
        self.press_setting.show()
        self.press_setting.lab_press_show.setText(sender.text())


    """参数（配方）配置函数"""
    def formula_process(self):
        """处理参数（配方）的函数"""
        self.auto_client_list = []
        self.lab_work_pos_show_list = []  # 存储所有显示标签的列表
        self.btn_call_formula_list = []  # 存储所有调用配方按钮的列表
        self.btn_edit_formula_list = []  # 存储所有编辑配方按钮的列表
        self.btn_load_formula_list = []  # 存储所有调用配方按钮的列表
        self.get_lists()  # 获得显示标签、调用配方、编辑配方和装载配方列表
        self.current_work_pos_list = []  # 模拟堆栈临时存储当前配方
        self.current_formula_dict = {}  # 存储工位当前调用配方

        for i in self.btn_call_formula_list:  # 给调用配方按钮绑定配方列表槽函数
            eval(i).clicked.connect(self.formula_list_show)
        for i in self.btn_edit_formula_list:  # 给编辑配方按钮绑定编辑界面槽函数
            eval(i).clicked.connect(self.edit_formula_show)
        for i in self.btn_load_formula_list:  # 给装载配方按钮绑定装载配符槽函数
            eval(i).clicked.connect(self.load_formula_show)

    def get_lists(self):
        """获得显示标签、调用配方、编辑配方和装载配方列表"""
        for i in range(1, self.total_work_poses+1):
            self.lab_work_pos_show_list.append('self.lab_work_pos_show{}'.format(i))
            self.btn_call_formula_list.append('self.btn_call_formula{}'.format(i))
            self.btn_edit_formula_list.append('self.btn_edit_formula{}'.format(i))
            self.btn_load_formula_list.append('self.btn_load_formula{}'.format(i))
            self.auto_client_list.append('self.auto_client_{}'.format(i))

    def formula_list_show(self):
        """弹出配方列表"""
        sender = self.sender()
        self.current_work_pos_list.append(sender.objectName())  # 临时存储当前工位信息
        self.formula_li = FormulaList()  # 实例化配方列表
        self.formula_li.show()
        self.formula_li.listView.clicked.connect(self.formula_show)  # 给选择的配方绑定显示槽函数

    def formula_show(self, index):
        """显示已调用配方"""
        work_pos = self.current_work_pos_list.pop()
        work_pos_index = eval(work_pos[work_pos.index('u') + 3:])
        current_lab = eval(self.lab_work_pos_show_list[work_pos_index - 1])
        current_formula = self.formula_li.formula_list[index.row()]
        text = '{}'.format(current_formula[current_formula.index('：') + 1:current_formula.index('（')])
        current_lab.setText(text)  # 将当前标签显示为配方名字
        formula_index = eval(current_formula[current_formula.index('方') + 1:current_formula.index('：')])
        self.current_formula_dict[work_pos_index] = formula_index  # 将当前工位与当前调用配方组成键值对
        self.formula_li.close()

    def edit_formula_show(self):
        """弹出编辑配方窗口"""
        sender = self.sender()
        btn_name = sender.objectName()
        work_pos_index = eval(btn_name[btn_name.index('u') + 3:])
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
        btn_name = sender.objectName()
        try:
            work_pos_index = eval(btn_name[btn_name.index('u') + 3:])
            formula_index = self.current_formula_dict[work_pos_index]
            self.edit_for = EditFormula(formula_index)  # 实例化编辑配方
            # 自动测试更新运行时间
            self.auto_time_update = AutoTimeUpdate(work_pos_index)
            self.auto_time_update.time_update.connect(self.auto_time_show)
            self.auto_time_update.start()
            # 自动测试通讯
            if work_pos_index == 1:
                self.auto_client_1 = AutoClient(work_pos_index, formula_index, self.edit_for.total_steps)
            elif work_pos_index == 2:
                self.auto_client_2 = AutoClient(work_pos_index, formula_index, self.edit_for.total_steps)
            elif work_pos_index == 3:
                self.auto_client_3 = AutoClient(work_pos_index, formula_index, self.edit_for.total_steps)
            elif work_pos_index == 4:
                self.auto_client_4 = AutoClient(work_pos_index, formula_index, self.edit_for.total_steps)
            eval(self.auto_client_list[work_pos_index-1]).data_list = self.edit_for.formula_data_array[formula_index][0:self.edit_for.total_steps]
            eval(self.auto_client_list[work_pos_index - 1]).client.connect(self.auto_test)
            eval(self.auto_client_list[work_pos_index - 1]).pass_count.connect(self.update_pos)
            eval(self.auto_client_list[work_pos_index - 1]).hide_pass_count.connect(self.update_pass)
            eval(self.lab_work_pos_show_list[work_pos_index - 1]).setStyleSheet('color: rgb(255, 0, 0);\n''background-color: rgb(0, 0, 0);')
        except:  # 还没调用配方
            QMessageBox.warning(self, '操作失败！', '请先调用一个配方！')

    """自动测试配置函数"""
    def auto_test_process(self):
        """处理自动测试的函数"""
        self.tabWidget_1.installEventFilter(self)  # 添加事件过滤器
        self.tabWidget_2.installEventFilter(self)  # 添加事件过滤器
        self.lab_auto_time_list = []
        self.lab_auto_abcd_list = [[], [], [], []]
        self.lab_auto_abcd1_list = [[], [], [], []]
        self.lab_auto_abcd2_list = [[], [], [], []]
        self.lab_auto_min_press_list = []
        self.lab_auto_leak_list = []
        self.lab_auto_torque_list = []
        self.lab_auto_pass_list = []
        self.current_test = []
        for i in range(1, 4+1):
            self.current_test.append(100)
            self.lab_auto_time_list.append('self.lab_auto_time_{}'.format(i))
            self.lab_auto_abcd_list[0].append('self.lab_auto_a_{}'.format(i))
            self.lab_auto_abcd_list[1].append('self.lab_auto_b_{}'.format(i))
            self.lab_auto_abcd_list[2].append('self.lab_auto_c_{}'.format(i))
            self.lab_auto_abcd_list[3].append('self.lab_auto_d_{}'.format(i))
            self.lab_auto_abcd1_list[0].append('self.lab_auto_a1_{}'.format(i))
            self.lab_auto_abcd1_list[1].append('self.lab_auto_b1_{}'.format(i))
            self.lab_auto_abcd1_list[2].append('self.lab_auto_c1_{}'.format(i))
            self.lab_auto_abcd1_list[3].append('self.lab_auto_d1_{}'.format(i))
            self.lab_auto_abcd2_list[0].append('self.lab_auto_a2_{}'.format(i))
            self.lab_auto_abcd2_list[1].append('self.lab_auto_b2_{}'.format(i))
            self.lab_auto_abcd2_list[2].append('self.lab_auto_c2_{}'.format(i))
            self.lab_auto_abcd2_list[3].append('self.lab_auto_d2_{}'.format(i))
            self.lab_auto_min_press_list.append('self.lab_auto_min_press_{}'.format(i))
            self.lab_auto_leak_list.append('self.lab_auto_leak_{}'.format(i))
            self.lab_auto_torque_list.append('self.lab_auto_torque_{}'.format(i))
            self.lab_auto_pass_list.append('self.lab_auto_pass_{}'.format(i))

    def auto_test(self, work_pos_index, slot):
        slot_list = slot.split(',')
        which_test = eval(slot_list[-1])
        if which_test != -1:
            self.current_test[work_pos_index] = which_test
            for i in range(4):
                if i == which_test:
                    eval(self.lab_auto_abcd1_list[i][work_pos_index]).setStyleSheet('color: rgb(255, 0, 0);\n''background-color: rgb(0, 0, 0);')
                    eval(self.lab_auto_abcd2_list[i][work_pos_index]).setStyleSheet('color: rgb(255, 0, 0);\n''background-color: rgb(0, 0, 0);')
                    eval(self.lab_auto_abcd_list[i][work_pos_index]).setStyleSheet('color: rgb(255, 0, 0);\n''background-color: rgb(0, 0, 0);')
                else:
                    eval(self.lab_auto_abcd1_list[i][work_pos_index]).setStyleSheet('color: rgb(0, 0, 0);\n''background-color: rgb(220, 220, 220);')
                    eval(self.lab_auto_abcd2_list[i][work_pos_index]).setStyleSheet('color: rgb(0, 0, 0);\n''background-color: rgb(220, 220, 220);')
                    eval(self.lab_auto_abcd_list[i][work_pos_index]).setStyleSheet('color: rgb(0, 0, 0);\n''background-color: rgb(220, 220, 220);')
        try:
            for i in range(4):
                if i == self.current_test[work_pos_index]:
                    eval(self.lab_auto_abcd1_list[i][work_pos_index]).setText(slot_list[0])
                    eval(self.lab_auto_abcd2_list[i][work_pos_index]).setText(slot_list[1])
                else:
                    eval(self.lab_auto_abcd1_list[i][work_pos_index]).setText('0')
                    eval(self.lab_auto_abcd2_list[i][work_pos_index]).setText('0')
        except:
            pass
        eval(self.lab_auto_min_press_list[work_pos_index]).setText(slot_list[2])
        eval(self.lab_auto_leak_list[work_pos_index]).setText(slot_list[3])
        eval(self.lab_auto_torque_list[work_pos_index]).setText(slot_list[4])

    def auto_time_show(self, work_pos_index, show_time):
        """自动测试更新运行时间"""
        eval(self.lab_auto_time_list[work_pos_index - 1]).setText(show_time)

    def update_pass(self, work_pos_index):
        eval(self.lab_auto_pass_list[work_pos_index]).setText('')
        eval(self.lab_auto_pass_list[work_pos_index]).setStyleSheet('color: rgb(0, 0, 0);\n''background-color: rgb(220, 220, 220);')

    def eventFilter(self, object, event):
        """给lineEdit添加单击左键事件过滤器"""
        if object == self.tabWidget_2 or object == self.tabWidget_1:
            if event.type() == QMouseEvent.MouseButtonPress:
                mouse_event = QMouseEvent(event)
                if mouse_event.buttons() == Qt.LeftButton:
                    if object == self.tabWidget_2:
                        self.test_state.emit(0)
                    elif object == self.tabWidget_1:
                        self.test_state.emit(1)
        return QWidget.eventFilter(self, object, event)

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
        self.data_count_init()  # 计数器线程

    def data_count_init(self):
        """计数器线程"""
        self.data_count = DataCount()  # 创建线程
        # self.data_count.update_date.connect(self.update_pos)  # 连接信号
        self.data_count.start()  # 开始线程

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
        work_pos = sender.objectName()
        work_pos_index = eval(work_pos[work_pos.index('r') + 2:])
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

    def update_pos(self, i, j):
        """模拟计数器"""
        if j == 0:
            eval(self.lab_auto_pass_list[i - 1]).setText('合格')
            eval(self.lab_auto_pass_list[i - 1]).setStyleSheet('color: rgb(255, 0, 0);\n''background-color: rgb(0, 0, 0);')
        update_list = [i, 0, -1]
        for i in update_list:
            self.data_count_data_list[i][j] += 1
            self.update_data_count(i)

    def update_data_count(self, i):
        """对修改的标签进行更新"""
        self.data_count_data_list[i][2] = self.data_count_data_list[i][0] + self.data_count_data_list[i][1]
        self.data_count_data_list[i][3] = '{:.2f}%'.format(self.data_count_data_list[i][0] / self.data_count_data_list[i][2] * 100) \
            if self.data_count_data_list[i][2] != 0 else '{:.2f}%'.format(0)
        for j in range(self.total_work_poses + 2):  # 将计数标签显示相应结果
            for i in range(4):
                eval(self.lab_count_list[i][j]).setText(str(self.data_count_data_list[j][i]))

    def data_count_show(self):
        """显示初始计数"""
        for j in range(1, self.total_work_poses + 1):  # 单工位总数=合格数+不合格数
            self.data_count_data_list[j][2] = self.data_count_data_list[j][0] + self.data_count_data_list[j][1]
        for i in range(3):  # 总计数的合格数、不合格数、总数由各工位计数相加得到
            for j in range(1, self.total_work_poses + 1):
                self.data_count_data_list[0][i] += self.data_count_data_list[j][i]
                self.data_count_data_list[-1][i] += self.data_count_data_list[j][i]
        for i in range(self.total_work_poses + 2):  # 合格率由合格数与总数比值所得，默认合格率为0
            self.data_count_data_list[i][3] = '{:.2f}%'.format(self.data_count_data_list[i][0] / self.data_count_data_list[i][2] * 100) \
                if self.data_count_data_list[i][2] != 0 else '{:.2f}%'.format(0)
        for j in range(self.total_work_poses + 2):  # 将计数标签显示相应结果
            for i in range(4):
                eval(self.lab_count_list[i][j]).setText(str(self.data_count_data_list[j][i]))


    """数据处理配置函数"""
    def data_process(self):
        """处理数据配置的函数"""
        self.btn_data_process_list = []  # 存储所有工位的列表
        self.tableView_model()  # 创建QTableView表格，并添加自定义模型
        for i in range(1, self.total_work_poses+1):  # 获得工位列表
            self.btn_data_process_list.append('self.btn_data_process_{}'.format(i))
        for i in self.btn_data_process_list:  # 给工位绑定槽函数
            eval(i).clicked.connect(self.data_process_show)
        self.btn_data_process_set.clicked.connect(self.data_set_show)  # 点击设置弹出设置界面

    def tableView_model(self):
        """创建QTableView表格，并添加自定义模型"""
        self.para_list = ['动作阀1', '动作阀2', '动作阀3', '动作阀4', '动作阀5', '动作阀6',
                          '伺服', '伺服转矩(N·M)', '伺服速度(r/S)', '伺服打开角度(°)',
                          '高压', '低压', '流量阀', '密封', '排气', '过渡阀A', '过渡阀B', '过渡阀C', '过渡阀D',
                          '最低工作压力(mbar)', '大漏值(pa)', '测压ΔP1(pa)/时间(1S)', '稳压ΔP2(pa)/时间(1S)']
        self.title_list = ['1', '2', '3', '4', '5', '6']
        self.model = QStandardItemModel(len(self.para_list), len(self.title_list))
        self.model.setHorizontalHeaderLabels(self.title_list)
        self.model.setVerticalHeaderLabels(self.para_list)
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)  # 表格填充窗口
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.verticalHeader().setStretchLastSection(True)  # 表格填充窗口
        self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def data_process_show(self):
        sender = self.sender()
        btn_name = sender.objectName()
        sender.setStyleSheet('background-color: rgb(255, 0, 0);\n''color: rgb(255, 255, 255);')
        for i in self.btn_data_process_list:
            if i != self.btn_data_process_list[eval(btn_name[btn_name.index('c') + 5:]) - 1]:
                eval(i).setStyleSheet('background-color: rgb(220, 220, 220);\n''color: rgb(0, 0, 0);')

    def data_set_show(self):
        self.setting = DataSet()
        self.setting.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


class DataCount(QThread):
    update_date = pyqtSignal(int, int)

    def run(self):
        while True:
            for i in range(1, 21):
                for j in range(2):
                    self.update_date.emit(i, j)
                    time.sleep(0.5)


class AutoTimeUpdate(QThread):
    """自动测试更新运行时间"""
    time_update = pyqtSignal(int, str)

    def __init__(self, work_pos_index):
        super().__init__()
        self.work_pos_index = work_pos_index

    def run(self):
        start = time.perf_counter()
        while True:
            time.sleep(1)
            total_time = time.perf_counter() - start
            second = total_time % 60
            minute = total_time // 60 % 60
            hour = total_time // 3600 % 24
            show_time = '{:0>2.0f}:{:0>2.0f}:{:0>2.0f}'.format(hour, minute, second)
            self.time_update.emit(self.work_pos_index, show_time)


class AutoClient(QThread):
    """自动测试通讯"""
    client = pyqtSignal(int, str)
    pass_count = pyqtSignal(int, int)
    hide_pass_count = pyqtSignal(int)

    def __init__(self, work_pos_index, formula_index, total_steps):
        super().__init__()
        self.work_pos_index, self.formula_index, self.total_steps = work_pos_index - 1, formula_index, total_steps
        self.data_list = []
        self.para_list = ['动作阀1', '动作阀2', '动作阀3', '动作阀4', '动作阀5', '动作阀6',
                          '伺服', '伺服转矩(N·M)', '伺服速度(r/S)', '伺服打开角度(°)',
                          '高压', '低压', '流量阀', '密封', '排气', '过渡阀A', '过渡阀B', '过渡阀C', '过渡阀D',
                          '测压ΔP1(pa)/时间(1S)', '稳压ΔP2(pa)/时间(1S)', '最低工作压力(mbar)', '大漏值(pa)']
        self.codesys_formula_address_list = []
        for i in range(len(self.para_list)):
            self.codesys_formula_address_list.append(0)
        self.codesys_work_pos_list = []
        self.running = 0
        for i in range(20):
            self.codesys_work_pos_list.append(self.codesys_formula_address_list)

    def servo_set(self, i):
        for j in range(1, 4):
            if self.codesys_work_pos_list[self.work_pos_index][i + j] == self.data_list[self.current_step][i + j][0]:
                pass
            else:
                self.codesys_work_pos_list[self.work_pos_index][i + j] = self.data_list[self.current_step][i + j][0]

    def run(self):
        while self.running:
            error_step_list = []  # 记录报警步数
            self.count = 0
            try:  # 开始通信
                self.current_step = 0  # 记录当前步数
                start = time.perf_counter()  # 开始第一步计时
                while self.current_step < self.total_steps and self.running:
                    which_test = [0, 0, 0, 0]
                    all_test = ['过渡阀A', '过渡阀B', '过渡阀C', '过渡阀D']
                    else_test = ['伺服', '伺服转矩(N·M)', '伺服速度(r/S)', '伺服打开角度(°)',
                                 '测压ΔP1(pa)/时间(1S)', '稳压ΔP2(pa)/时间(1S)', '最低工作压力(mbar)', '大漏值(pa)']
                    self.slot = '{},{},{:.2f},{:.2f},{:.2f}'.format(0, 0, 0, 0, 0)
                    for i in range(len(self.para_list)):
                        if self.running:
                            if self.para_list[i] not in else_test[1:]:
                                if self.data_list[self.current_step][i][0] == 1:  # 配方信息等于1表示该属性得电
                                    if self.para_list[i] == else_test[0]:  # 伺服得电
                                        self.servo_set(i)
                                    if self.para_list[i] in all_test:  # 根据过渡阀得电情况判断测试哪个阀
                                        which_test[all_test.index(self.para_list[i])] = 1
                                    self.keep_time = self.data_list[self.current_step][i][1]
                                    # get相应参数当前值
                                    self.slot = '{},{},{:.2f},{:.2f},{:.2f}'.format(self.codesys_work_pos_list
                                        [self.work_pos_index][i], self.count, time.perf_counter(), start, self.keep_time)
                                    # 判断相应参数是否一致
                                    if self.codesys_work_pos_list[self.work_pos_index][i] == '得电':
                                        pass
                                    else:  # 将相应参数set
                                        self.codesys_work_pos_list[self.work_pos_index][i] = '得电'
                                elif self.data_list[self.current_step][i][0] == 2:  # 配方信息等于2表示该属性失电
                                    if self.para_list[i] == else_test[0]:  # 伺服失电
                                        self.servo_set(i)
                                    if self.para_list[i] in all_test:
                                        which_test[all_test.index(self.para_list[i])] = 2
                                    self.keep_time = self.data_list[self.current_step][i][1]
                                    # get相应参数当前值
                                    self.slot = '{},{},{:.2f},{:.2f},{:.2f}'.format(self.codesys_work_pos_list
                                         [self.work_pos_index][i], self.count, time.perf_counter(), start, self.keep_time)
                                    # 判断相应参数是否一致
                                    if self.codesys_work_pos_list[self.work_pos_index][i] == '失电':
                                        pass
                                    else:  # 将相应参数set
                                        self.codesys_work_pos_list[self.work_pos_index][i] = '失电'
                            elif self.para_list[i] in ['测压ΔP1(pa)/时间(1S)', '稳压ΔP2(pa)/时间(1S)']:
                                if self.data_list[self.current_step][i][0] != 0:  # 开始检测
                                    self.keep_time = self.data_list[self.current_step][i][1]
                                    self.slot = '{},{},{:.2f},{:.2f},{:.2f}'.format(self.codesys_work_pos_list
                                    [self.work_pos_index][i], self.count, time.perf_counter(), start, self.keep_time)
                        else:
                            break
                    if which_test in [[2, 1, 1, 1], [1, 2, 1, 1], [1, 1, 2, 1], [1, 1, 1, 2]]:
                        self.slot += ',{}'.format(which_test.index(2))
                    else:
                        self.slot += ',{}'.format(-1)
                    if time.perf_counter() - start >= self.keep_time:  # 达到延迟时间，结束当前步循环
                        self.current_step += 1
                        start = time.perf_counter()  # 下一步重新计时
                        if self.current_step == self.total_steps:  # 当前工件测试完成
                            self.count += 1  # 合格数加1
                            self.pass_count.emit(self.work_pos_index + 1, 0)
                            self.current_step = 0
                            time.sleep(0.5)
                            self.hide_pass_count.emit(self.work_pos_index)
                    self.client.emit(self.work_pos_index, self.slot)
                    time.sleep(0.05)  # 每0.05秒刷新一次
                    error_step_list.append(self.current_step)
            except:
                current_step = error_step_list.pop() if len(error_step_list) else 0
                print('配方第{}步有误！'.format(current_step + 1))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = MyWindow(20)
    # my_show.showFullScreen()  # 全屏显示
    my_show.show()
    sys.exit(app.exec_())
