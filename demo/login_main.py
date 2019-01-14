import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent

from login import Ui_Login
from main import MyWindow
from edit_formula import EditFormula
from input_name_main import InputName  # 导入名字键盘类


class Login(QWidget, Ui_Login):
    """登陆界面"""

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.width_, self.height_ = 300, 120
        self.setting()
        self.login_process()

    def setting(self):
        self.screen_rect = QApplication.desktop().screenGeometry()  # 获取显示器分辨率大小
        self.screen_height = self.screen_rect.height()
        self.screen_width = self.screen_rect.width()
        self.setGeometry((self.screen_width - self.width_) // 2, (self.screen_height - self.height_) // 2 - 2 * self.height_ + 20, self.width_, self.height_)
        self.setWindowModality(Qt.ApplicationModal)  # 应用程序模态，程序未完成当前对话框时，阻止和任何其他窗口进行交互
        self.setWindowFlags(Qt.WindowCloseButtonHint)  # 只显示关闭按钮
        self.setFixedSize(self.width(), self.height())  # 禁止拉伸窗口大小

    def login_process(self):
        self.user_admin = 0  # 判断是否是管理员登录
        self.user_login = 0  # 判断模式（0：登录模式，1：验证登录模式，2：修改模式，3：验证修改模式）
        self.current_lineEdit = []  # 模拟堆栈临时存储用户名或口令
        self.edit_for = EditFormula()
        self.total_formulas = self.edit_for.total_formulas
        self.user_info_list = self.edit_for.formula_name_and_steps_list  # 存储用户信息
        passwd = self.user_info_list[self.total_formulas+1][0]
        self.user_info_list[self.total_formulas+1][0] = '13023686323' if passwd == 'new' else passwd
        self.comboBox_login.addItems(['系统管理员', str(self.user_info_list[self.total_formulas][0])])  # 添加用户信息
        self.comboBox_login.activated.connect(self.users_changed)  # 添加用户名改变信号槽
        self.lineEdit_login_user.installEventFilter(self)  # 安装事件过滤器，监控单击事件
        self.lineEdit_login_passwd.installEventFilter(self)  # 安装事件过滤器，监控单击事件
        self.lineEdit_login_passwd.setEchoMode(QLineEdit.Password)  # 设置密码形式显示
        self.btn_login_ok.clicked.connect(self.login_ok)  # 核实登录信息是否正确
        self.btn_login_cancel.clicked.connect(self.login_cancel)  # 清除密码或确认修改
        self.btn_login_users_manage.clicked.connect(self.users_manage)  # 切换模式

    def users_changed(self):
        """选择用户"""
        if self.user_login == 2:  # 如果是修改模式
            # if not self.user_admin:
            if self.comboBox_login.currentText() == '系统管理员':
                QMessageBox.warning(self, '选择错误！', '您不可以修改用户管理员信息！')
            else:
                self.lineEdit_login_user.setText(self.comboBox_login.currentText())
        else:
            self.lineEdit_login_user.setText(self.comboBox_login.currentText())

    def login_ok(self):
        """核实信息是否正确"""
        if self.user_login == 0:
            self.login_check()
        elif self.user_login == 1:
            self.change_user_login()
        elif self.user_login == 2:
            self.change_user_ok()
        else:
            self.change_user_ok_double()

    def login_check(self):
        """核实登录信息是否正确"""
        if (self.lineEdit_login_user.text(), self.lineEdit_login_passwd.text()) == ('系统管理员', '1'):
            QMessageBox.information(self, '登录成功！', '欢迎系统管理员登录！')
            self.close()
            self.user_admin = 1
            self.my_window_show = MyWindow(20)
            # self.my_window_show.showFullScreen()  # 全屏显示
            self.my_window_show.show()
            self.save_user_info()
        elif (self.lineEdit_login_user.text(), self.lineEdit_login_passwd.text()) == \
                (str(self.user_info_list[self.total_formulas][0]), str(self.user_info_list[self.total_formulas+1][0])):
            QMessageBox.information(self, '登录成功！', '欢迎{}登录！'.format(self.lineEdit_login_user.text()))
            self.close()
            self.user_admin = 0
            self.my_window_show = MyWindow(20)
            # self.my_window_show.showFullScreen()  # 全屏显示
            self.my_window_show.show()
            self.save_user_info()
        else:
            QMessageBox.warning(self, '输入错误！', '请检查用户名或口令！')
            self.lineEdit_login_user.clear()
            self.lineEdit_login_passwd.clear()

    def change_user_login(self):
        """核实验证信息是否正确"""
        if (self.lineEdit_login_user.text(), self.lineEdit_login_passwd.text()) == ('系统管理员', '1'):
            QMessageBox.information(self, '通过验证！', '请输入新的用户名或口令！')
            self.user_admin = 1
            self.user_login = 2  # 切换到修改模式
            self.btn_login_ok.setText('确认修改')
            self.comboBox_login.setCurrentText(self.user_info_list[self.total_formulas][0])
            self.lineEdit_login_user.setText(self.user_info_list[self.total_formulas][0])
            self.lineEdit_login_passwd.clear()
        elif (self.lineEdit_login_user.text(), self.lineEdit_login_passwd.text()) == \
                (self.user_info_list[self.total_formulas][0], self.user_info_list[self.total_formulas+1][0]):
            QMessageBox.information(self, '通过验证！', '请输入新的用户名或口令！')
            self.user_admin = 0
            self.user_login = 2
            self.btn_login_ok.setText('确认修改')
            self.comboBox_login.setCurrentText(self.user_info_list[self.total_formulas][0])
            self.lineEdit_login_user.setText(self.user_info_list[self.total_formulas][0])
            self.lineEdit_login_passwd.clear()
        else:
            QMessageBox.warning(self, '输入错误！', '请检查用户名或口令！')
            self.lineEdit_login_user.clear()
            self.lineEdit_login_passwd.clear()

    def change_user_ok(self):
        """确认修改用户信息"""
        try:
            user = self.lineEdit_login_user.text()
            passwd = self.lineEdit_login_passwd.text()
            if 0 < len(user) < self.edit_for.max_digit:
                self.user_info_list[self.total_formulas][0] = user
                if 5 < len(passwd) < self.edit_for.max_digit:
                    self.user_info_list[self.total_formulas + 1][0] = passwd
                    QMessageBox.information(self, '确认信息！', '请再次输入，注意两次保持一致！')
                    self.lineEdit_login_user.clear()
                    self.lineEdit_login_passwd.clear()
                    self.user_login = 3  # 切换到验证修改模式
                else:
                    QMessageBox.warning(self, '操作失败！', '请修改口令长度在6-{}之间！'.format(self.edit_for.max_digit-1))
            else:
                QMessageBox.warning(self, '操作失败！', '用户名不能为空且不超过{}位！'.format(self.edit_for.max_digit-1))
        except:
            QMessageBox.warning(self, '操作失败！', '请检查输入！')

    def change_user_ok_double(self):
        """验证修改"""
        user = self.lineEdit_login_user.text()
        passwd = self.lineEdit_login_passwd.text()
        if self.user_info_list[self.total_formulas][0] == user and self.user_info_list[self.total_formulas + 1][0] == passwd:
            self.save_user_info()  # 保存用户信息
        else:
            QMessageBox.warning(self, '操作失败！', '两次信息不一致，请重新输入！')
            self.lineEdit_login_user.clear()
            self.lineEdit_login_passwd.clear()
            self.user_login = 2  # 切换到修改模式

    def login_cancel(self):
        """清空密码"""
        self.lineEdit_login_passwd.clear()

    def users_manage(self):
        """切换模式"""
        self.lineEdit_login_user.clear()
        self.lineEdit_login_passwd.clear()
        if self.user_login == 0:  # 如果是登录模式
            QMessageBox.information(self, '进入验证页面！', '请首先登录一个用户！')
            self.user_login = 1  # 切换到验证登录模式
            self.btn_login_ok.setText('确认')
            self.btn_login_users_manage.setText('返回登录')
        else:
            self.user_login = 0  # 切换到登录模式
            self.btn_login_ok.setText('确认')
            self.btn_login_users_manage.setText('用户管理')

    def eventFilter(self, object, event):
        """给lineEdit添加单击左键事件过滤器"""
        if object == self.lineEdit_login_passwd or object == self.lineEdit_login_user:
            if event.type() == QMouseEvent.MouseButtonPress:
                mouse_event = QMouseEvent(event)
                if mouse_event.buttons() == Qt.LeftButton:
                    self.current_lineEdit.append(object)
                    self.input_name = InputName()
                    if object == self.lineEdit_login_passwd:
                        self.input_name.lineEdit_input.setEchoMode(QLineEdit.Password)  # 设置密码形式显示
                    self.input_name.btn_input_ok.clicked.connect(self.login_show)  # 将密码隐性显示在登录界面上
                    self.input_name.show()
        return QWidget.eventFilter(self, object, event)

    def login_show(self):
        """将密码隐性显示在登录界面上"""
        text = self.input_name.lineEdit_input.text()
        current_lineEdit = self.current_lineEdit.pop()
        current_lineEdit.setText(text)
        self.input_name.close()

    def save(self, i):
        """获得用户信息保存的索引和列表"""
        return (self.total_formulas+i) * self.edit_for.max_digit, self.edit_for.alp_to_num_code(self.user_info_list[self.total_formulas+i][0])

    def save_user_info(self):
        """保存用户信息"""
        try:
            self.edit_for.formula_name_and_steps_array[self.save(0)[0]] = self.user_admin
            if self.user_login == 3:
                for i in range(2):
                    self.edit_for.formula_name_and_steps_array[self.save(i)[0] + 1:self.save(i)[0] + 1 + len(self.save(i)[1])] = self.save(i)[1]
            self.edit_for.formula_data_array[0] = self.edit_for.formula_name_and_steps_array.reshape(self.edit_for.formula_name_and_steps_shape_save)
            self.edit_for.formula_data_array.tofile('formula.dat', format='%d')  # 保存
            if self.user_login == 3:
                self.comboBox_login.setItemText(1, str(self.user_info_list[self.total_formulas][0]))
                answer = QMessageBox.question(self, '修改成功！', '是否以该用户登录系统?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if answer == QMessageBox.Yes:
                    self.close()
                    self.my_window_show = MyWindow(20)
                    self.my_window_show.showFullScreen()
                else:
                    self.user_admin = 0
                    self.users_manage()  # 切换到登录界面
        except:
            QMessageBox.warning(self, '修改失败！', '用户信息修改失败！')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = Login()
    my_show.show()
    sys.exit(app.exec_())
