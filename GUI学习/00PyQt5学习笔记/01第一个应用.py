import sys
from PyQt5.QtWidgets import QApplication, QWidget

if __name__ == '__main__':

    """每一个PyQt5项目都需要创建一个QApplication对象，sys.argv提供了命令行的一些参数，
    这样Python脚本就能从Shell运行，这是我们控制脚本开始运行的方式"""
    app = QApplication(sys.argv)

    # QWidget是所有界面的基类，这里采用默认的构造函数（无父对象，没有父对象的widget也就是window）
    w = QWidget()

    # 用resize函数重设了窗口的大小为宽300，高200
    w.resize(300, 200)
    # move函数把窗口移动到了x=300,y=300的位置
    w.move(300, 300)

    # 设置了窗口的标题
    w.setWindowTitle('First PyQt5')

    # show函数让Simple这个窗口在屏幕中显示出来，这个窗口时先在内存中产生，然后再显示在屏幕中的
    w.show()

    """在开头我们设置了这个应用的主函数，事件由此开始产生，主函数从窗口系统接受事件并传递给widget应用，
    而当我们使用exit()或者关闭了widget时，主函数就终止；
    sys.exit()确保干净利落不留痕迹地退出；
    注意到这里的代码exec_()后面有个'_',这是因为exec是Python的关键字，为了避免冲突"""
    sys.exit(app.exec_())

