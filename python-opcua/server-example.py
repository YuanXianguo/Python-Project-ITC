from threading import Thread
import copy
import logging
from datetime import datetime
import time
from math import sin
import sys
sys.path.insert(0, "..")

try:
    from IPython import embed
except ImportError:
    import code

    def embed():
        myvars = globals()
        myvars.update(locals())
        shell = code.InteractiveConsole(myvars)
        shell.interact()


from opcua import ua, uamethod, Server


# class SubHandler(object):
#
#     """
#     订阅处理程序。 从服务器接收订阅的事件
#     """
#
#     def datachange_notification(self, node, val, data):
#         print("Python: New data change event", node, val)
#
#     def event_notification(self, event):
#         print("Python: New event", event)


# 通过服务器公开的方法

def func(parent, variant):
    ret = False
    if variant.Value % 2 == 0:
        ret = True
    return [ua.Variant(ret, ua.VariantType.Boolean)]


# 通过服务器公开的方法
# 使用装饰器自动转换为变体

@uamethod
def multiply(parent, x, y):
    print("multiply method call with parameters: ", x, y)
    return x * y


class VarUpdater(Thread):
    def __init__(self, var):
        Thread.__init__(self)
        self._stopev = False
        self.var = var

    def stop(self):
        self._stopev = True

    def run(self):
        while not self._stopev:
            v = sin(time.time() / 10)
            self.var.set_value(v)
            time.sleep(0.1)


if __name__ == "__main__":
    # # 可选：设置日志记录
    # logging.basicConfig(level=logging.WARN)
    # # logger = logging.getLogger("opcua.address_space")
    # # logger.setLevel(logging.DEBUG)
    # # logger = logging.getLogger("opcua.internal_server")
    # # logger.setLevel(logging.DEBUG)
    # # logger = logging.getLogger("opcua.binary_server_asyncio")
    # # logger.setLevel(logging.DEBUG)
    # # logger = logging.getLogger("opcua.uaprocessor")
    # # logger.setLevel(logging.DEBUG)

    # 现在设置我们的服务器
    server = Server()
    # server.disable_clock()
    # server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")
    server.set_endpoint("opc.tcp://0.0.0.0:502/")
    server.set_server_name("FreeOpcUa Example Server")
    # 为客户端设置所有可能的端点策略以进行连接
    server.set_security_policy([
                ua.SecurityPolicyType.NoSecurity,
                ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
                ua.SecurityPolicyType.Basic256Sha256_Sign])

    # 设置自己的命名空间
    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)

    # 创建一个我们可以在地址空间中实例化的新节点类型
    dev = server.nodes.base_object_type.add_object_type(idx, "MyDevice")
    dev.add_variable(idx, "sensor1", 1.0).set_modelling_rule(True)
    dev.add_property(idx, "device_id", "0340").set_modelling_rule(True)
    ctrl = dev.add_object(idx, "controller")
    ctrl.set_modelling_rule(True)
    ctrl.add_property(idx, "state", "Idle").set_modelling_rule(True)

    # 填充我们的地址空间

    # 首先是一个组织我们节点的文件夹
    myfolder = server.nodes.objects.add_folder(idx, "myEmptyFolder")
    # instanciate我们的设备的一个实例
    mydevice = server.nodes.objects.add_object(idx, "Device0001", dev)
    # get proxy to我们的设备状态变量
    mydevice_var = mydevice.get_child(["{}:controller".format(idx), "{}:state".format(idx)])

    # 直接创建一些对象和变量
    myobj = server.nodes.objects.add_object(idx, "MyObject")

    myvar = myobj.add_variable(idx, "MyVariable", 6.7)
    mysin = myobj.add_variable(idx, "MySin", 0, ua.VariantType.Float)
    myvar.set_writable()    # Set MyVariable to be writable by clients
    mystringvar = myobj.add_variable(idx, "MyStringVariable", "Really nice string")
    print(mystringvar.get_value())
    mystringvar.set_writable()    # Set MyVariable to be writable by clients
    mydtvar = myobj.add_variable(idx, "MyDateTimeVar", datetime.utcnow())
    mydtvar.set_writable()    # Set MyVariable to be writable by clients
    myarrayvar = myobj.add_variable(idx, "myarrayvar", [6.7, 7.9])
    myarrayvar = myobj.add_variable(idx, "myStronglytTypedVariable", ua.Variant([], ua.VariantType.UInt32))
    myprop = myobj.add_property(idx, "myproperty", "I am a property")
    mymethod = myobj.add_method(idx, "mymethod", func, [ua.VariantType.Int64], [ua.VariantType.Boolean])
    multiply_node = myobj.add_method(idx, "multiply", multiply, [ua.VariantType.Int64, ua.VariantType.Int64], [ua.VariantType.Int64])

    # 从xml导入一些节点
    server.import_xml("custom_nodes.xml")

    # 创建默认事件对象
    # 事件对象将自动拥有所有事件属性的成员
    # 您可能想要创建自定义事件类型，请参阅其他示例
    myeven = server.get_event_generator()
    myeven.event.Severity = 300

    # starting!
    server.start()
    print("Available loggers are: ", logging.Logger.manager.loggerDict.keys())
    vup = VarUpdater(mysin)  # 只是一个stupide类更新变量
    vup.start()
    try:
        # 如果要订阅服务器端的节点，请启用以下功能
        # handler = SubHandler()
        # sub = server.create_subscription(500, handler)
        # handle = sub.subscribe_data_change(myvar)
        # 触发事件，所有订阅的客户端都将收到它
        var = myarrayvar.get_value()  # 在db服务器端返回ref值！ 不是副本！
        var = copy.copy(var)  # 警告：我们需要在再次写入之前复制，否则不会生成数据更改事件
        var.append(9.3)
        myarrayvar.set_value(var)
        mydevice_var.set_value("Running")
        myeven.trigger(message="This is BaseEvent")
        server.set_attribute_value(myvar.nodeid, ua.DataValue(9.9))  # 服务器端写入方法，但比使用set_value快

        embed()
    finally:
        vup.stop()
        server.stop()
