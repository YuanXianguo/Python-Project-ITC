import time
import socket
from PyQt5.QtCore import pyqtSignal, QThread, QTimer


class StartTest(QThread):
    """模拟开始测试或急停"""
    start_signal = pyqtSignal(int, int)

    def __init__(self, work_pos_index):
        super().__init__()
        self.work_pos_index = work_pos_index
        self.running = 1
        self.start_signal_list = []
        for i in range(4):
            self.start_signal_list.append([0, 0])

    def run(self):
        while self.running:
            if (self.start_signal_list[self.work_pos_index][0] == 1
                    and self.start_signal_list[self.work_pos_index][1] == 0):
                self.start_signal.emit(self.work_pos_index, 1)
                self.start_signal_list[self.work_pos_index][0] = 0
            elif self.start_signal_list[self.work_pos_index][1] == 1:
                self.start_signal.emit(self.work_pos_index, 0)
                self.start_signal_list[self.work_pos_index][1] = 0
            time.sleep(0.004)
        else:
            self.start_signal.emit(-1, 2)  # self.running=0，表示切换到手动页面


class ManualClient(QThread):
    """手动测试通信客户端"""
    man_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.stack = []
        self.man_run_flag = False

    def run(self):
        manual_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while self.man_run_flag:
            try:
                self.send_msg = self.stack.pop()
                manual_socket.sendto(self.send_msg.encode("utf-8"), ("127.0.0.1", 1080))
            except:
                pass
            time.sleep(0.004)
        manual_socket.close()


class ManualServer(QThread):
    """手动测试通信服务器"""
    man_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.man_run_flag = False

    def run(self):
        manual_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        manual_socket.setblocking(False)
        manual_socket.bind(("127.0.0.1", 1060))
        while self.man_run_flag:
            try:
                rec_msg = manual_socket.recvfrom(256)[0].decode("utf-8")
                self.man_signal.emit(rec_msg)
            except:
                pass
            time.sleep(0.004)
        manual_socket.close()


class AutoClient(QThread):
    """自动测试通讯"""
    client_signal = pyqtSignal(int, str)
    pass_count_signal = pyqtSignal(int, int)
    error_signal = pyqtSignal(int, str)

    def __init__(self, work_pos_index, formula_index, formula_steps):
        super().__init__()
        self.work_pos_index = work_pos_index
        self.formula_index = formula_index
        self.formula_steps = formula_steps
        self.run_flag = 1
        self.count = 0
        self.state_flag = 1
        self.data_list = []
        self.para_list = ['动作阀1', '动作阀2', '动作阀3', '动作阀4', '动作阀5', '动作阀6',
                          '伺服', '伺服转矩(N·M)', '伺服速度(r/S)', '伺服打开角度(°)',
                          '高压', '低压', '流量阀', '密封', '排气', '过渡阀A', '过渡阀B', '过渡阀C', '过渡阀D',
                          '测压ΔP1(pa)/时间(1S)', '稳压ΔP2(pa)/时间(1S)', '最低工作压力(mbar)', '大漏值(pa)']
        self.else_test = ['伺服', '伺服转矩(N·M)', '伺服速度(r/S)', '伺服打开角度(°)',
                          '测压ΔP1(pa)/时间(1S)', '稳压ΔP2(pa)/时间(1S)', '最低工作压力(mbar)', '大漏值(pa)']
        self.codesys_work_pos_list = [[0] * len(self.para_list)] * 20

    def servo_set(self, i):
        for j in range(1, 4):
            if self.codesys_work_pos_list[self.work_pos_index][i + j] \
                    == self.data_list[self.current_step][i + j][0]:
                pass
            else:
                self.codesys_work_pos_list[self.work_pos_index][i + j] \
                    = self.data_list[self.current_step][i + j][0]

    def run(self):
        try:  # 开始通信
            self.timeout = 0  # 判断是否超时
            self.text = ''
            self.which_test = '未知'
            self.current_step = 0  # 记录当前步数
            start = time.perf_counter()  # 开始第一步计时
            start_time = time.perf_counter()  # 记录开始时间
            while self.current_step < self.formula_steps and self.run_flag:
                if self.state_flag:
                    which_test = [0, 0, 0, 0]  # 判断测试哪个腔体
                    all_test = ['过渡阀A', '过渡阀B', '过渡阀C', '过渡阀D']
                    self.slot = '{},{},{:.2f},{:.2f},{:.2f}, {:0>2.0f}'.format(0, 0, 0, 0, 0, 0)
                    for i in range(len(self.para_list)):
                        if self.run_flag:
                            if self.para_list[i] not in self.else_test[1:]:
                                # 配方信息等于1表示该属性得电
                                if self.data_list[self.current_step][i][0] == 1:
                                    if self.para_list[i] == self.else_test[0]:
                                        self.servo_set(i)  # 伺服得电
                                    # 根据过渡阀得电情况判断测试哪个阀
                                    if self.para_list[i] in all_test:
                                        which_test[all_test.index(self.para_list[i])] = 1
                                    # 记录延迟时间
                                    self.keep_time = self.data_list[self.current_step][i][1]
                                    # get相应参数当前值
                                    self.slot = '{},{},{:.2f},{:.2f},{:.2f},{:0>2.0f}'.format(
                                        i, self.count, time.perf_counter(), start,
                                        time.perf_counter() * i, time.perf_counter() - start_time)
                                    # 判断相应参数是否一致
                                    if self.codesys_work_pos_list[self.work_pos_index][i] == '得电':
                                        pass
                                    else:  # 将相应参数set
                                        self.codesys_work_pos_list[self.work_pos_index][i] = '得电'
                                elif self.data_list[self.current_step][i][0] == 2:  # 配方信息等于2表示该属性失电
                                    if self.para_list[i] == self.else_test[0]:  # 伺服失电
                                        self.servo_set(i)
                                    if self.para_list[i] in all_test:
                                        which_test[all_test.index(self.para_list[i])] = 2
                                    self.keep_time = self.data_list[self.current_step][i][1]
                                    # get相应参数当前值
                                    self.slot = '{},{},{:.2f},{:.2f},{:.2f}, {:0>2.0f}'.format(
                                        i, self.count, time.perf_counter(), start,
                                        time.perf_counter() * i, time.perf_counter() - start_time)
                                    # 判断相应参数是否一致
                                    if self.codesys_work_pos_list[self.work_pos_index][i] == '失电':
                                        pass
                                    else:  # 将相应参数set
                                        self.codesys_work_pos_list[self.work_pos_index][i] = '失电'
                            elif self.para_list[i] in ['测压ΔP1(pa)/时间(1S)', '稳压ΔP2(pa)/时间(1S)']:
                                if self.data_list[self.current_step][i][0] != 0:  # 开始检测
                                    self.keep_time = self.data_list[self.current_step][i][1]
                                    self.slot = '{},{},{:.2f},{:.2f},{:.2f}, {:0>2.0f}'.format(
                                        i, self.count, time.perf_counter(), start,
                                        time.perf_counter() * i, time.perf_counter() - start_time)
                                if self.codesys_work_pos_list[self.work_pos_index][i] \
                                        < self.data_list[self.current_step][i][0]:
                                    if self.para_list[i] == '测压ΔP1(pa)/时间(1S)':
                                        self.text = '保气ΔP1泄露'
                                    else:
                                        self.text = '保气ΔP2泄露'
                                    self.reset(0)
                                    self.state_flag = 0
                                    break
                            elif self.para_list[i] in ['最低工作压力(mbar)', '大漏值(pa)']:
                                if self.codesys_work_pos_list[self.work_pos_index][i] \
                                        < self.data_list[self.current_step][i][0]:
                                    self.keep_time = self.data_list[self.current_step][i][1]
                                    self.slot = '{},{},{:.2f},{:.2f},{:.2f}, {:0>2.0f}'.format(
                                        i, self.count, time.perf_counter(), start,
                                        time.perf_counter() * i, time.perf_counter() - start_time)
                                    if self.para_list[i] == '最低工作压力(mbar)':
                                        self.text = '工作压力过低'
                                    else:
                                        self.text = '差压过高'
                                    self.reset(0)
                                    self.state_flag = 0
                                    break
                            else:
                                self.keep_time = self.data_list[self.current_step][i][1]
                                self.slot = '{},{},{:.2f},{:.2f},{:.2f}, {:0>2.0f}'.format(
                                    i, self.count, time.perf_counter(), start,
                                    time.perf_counter() * i, time.perf_counter() - start_time)
                    if which_test in [[2, 1, 1, 1], [1, 2, 1, 1], [1, 1, 2, 1], [1, 1, 1, 2]]:  # 判断测试哪一个腔体
                        self.slot += ',{}'.format(which_test.index(2))
                        self.which_test = chr(which_test.index(2) + 65)
                    else:
                        self.slot += ',{}'.format(-1)
                    # 达到延迟时间，结束当前步循环
                    if time.perf_counter() - start >= self.keep_time:
                        self.current_step += 1
                        start = time.perf_counter()  # 下一步重新计时
                        if self.current_step == self.formula_steps:  # 当前工件测试完成
                            self.count += 1  # 合格数加1
                    self.client_signal.emit(self.work_pos_index, self.slot)
                    if time.perf_counter() - start_time > 20:
                        self.text = '测试超时'
                        self.reset(0)
                        self.state_flag = 0
                    if not self.state_flag:
                        if self.text in ['保气ΔP1泄露', '保气ΔP2泄露']:
                            self.text = '{}腔{}'.format(self.which_test,
                                                       self.text)
                        self.pass_count_signal.emit(self.work_pos_index + 1, 1)
                        self.error_signal.emit(self.work_pos_index, self.text)
                time.sleep(0.005)
            if not self.run_flag:  # 按下急停
                self.text = '已急停'
                self.reset(1)
            else:
                self.text = '合格'
                self.pass_count_signal.emit(self.work_pos_index + 1, 0)
        except:
            self.text = '配方第{}步有误！'.format(self.current_step + 1)
        self.error_signal.emit(self.work_pos_index, self.text)

    def reset(self, num):
        """复位"""
        while self.current_step + num:
            for i in range(len(self.para_list)):
                if self.para_list[i] not in self.else_test[1:]:
                    # 配方信息等于1表示该属性得电
                    if self.data_list[self.current_step][i][0] == 1:
                        if self.para_list[i] == self.else_test[0]:  # 伺服得电
                            self.servo_set(i)
                        # get相应参数当前值
                        # 判断相应参数是否一致
                        if self.codesys_work_pos_list[self.work_pos_index][i] == '失电':
                            pass
                        else:  # 将相应参数set
                            self.codesys_work_pos_list[self.work_pos_index][i] = '失电'
            self.current_step -= 1


class SysTime(QThread):
    """显示系统时间"""
    sys_time_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.sys_time_signal.emit(current_time)
            time.sleep(1)
