import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import pyqtSignal, Qt
from MainWinSignalSlog import Ui_Form

class MyMainWindow(QMainWindow, Ui_Form):
    """调用类"""
    # 通过pyqtSignal()自定义三个信号
    help_signal = pyqtSignal(str)
    print_signal = pyqtSignal(list)
    # 声明一个多重载版本的信号，包括一个带int和str类型参数的信号，以及带str类型参数的信号
    preview_signal = pyqtSignal([int, str], [str])

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        # 自定义信号的连接
        self.help_signal.connect(self.show_help_message)
        self.print_signal.connect(self.print_paper)
        self.preview_signal[str].connect(self.preview_paper)
        self.preview_cmdsignal[int, str].connect(self.preview_paper_with_args)
        # 自定义槽函数
        self.printButton.clicked.connect(self.emit_print_signal)
        self.previewButton.clicked.connect(self.emit_preview_signal)

    def emit_preview_signal(self):
        """发射预览信号"""
        if self.previewStatus.isChecked() == True:
            self.preview_signal[int, str].emit(1080, 'Full Screen')
        elif self.previewStatus.isChecked() == False:
            self.preview_signal[str].emit('Preview')

    def emit_print_signal(self):
        """发射打印信号"""
        p_list = []
        p_list.append(self.numberSpinBox.value())
        p_list.append(self.styleCombo.currentText())
        self.print_signal.emit(p_list)

    def print_paper(self, list):
        """显示打印状态标签"""
        self.resultLabel.setText('打印：份数：{} 纸张：{}'.format(str(list[0]), str(list[1])))

    def preview_paper_with_args(self, style, text):
        """全屏预览"""
        self.resultLabel.setText(str(style)+text)

    def preview_paper(self, text):
        """当前预览"""
        self.resultLabel.setText(text)

    def keyPressEvent(self, event):
        """重载按键事件"""
        if event.key() == Qt.Key_F1:
            self.help_signal.emit('help message')

    def show_help_message(self, message):
        """显示帮助信息"""
        self.resultLabel.setText(message)
        self.statusBar().showMessage(message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = MyMainWindow()
    my_show.show()
    sys.exit(app.exec_())
