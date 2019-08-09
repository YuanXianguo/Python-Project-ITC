import sys,time
sys.path.insert(0, "..")
from opcua import Client,ua

if __name__ == "__main__":
    client = Client("opc.tcp://192.168.21.36:4840")
    # client = Client("opc.tcp://127.0.0.1:4840/freeopcua/server/")
    # client = Client("opc.tcp://admin@localhost:4840/freeopcua/server/") # connect using a user
    try:
        res = client.connect()

        # 客户端有一些方法可以获取UA节点的代理，这些节点应始终位于地址空间中，例如Root或Objects
        root = client.get_root_node()
        print("Objects node is: ", root)

        # 节点对象具有读取和写入节点属性以及浏览或填充地址空间的方法
        print("Children of root are: ", root.get_children())
        print("Children of Children of root are: ", root.get_children()[0].get_children())

        # 获取一个知道其节点ID的特定节点
        var = client.get_node(ua.NodeId(1002, 2))
        print(var)
        var = client.get_node("ns=3;i=2002")
        print(var)
        # var.get_data_value()  # 获取node的值作为DataValue对象
        # var.get_value()  # 获取节点的值作为python内置
        # var.set_value(ua.Variant([23], ua.VariantType.Int64))  # 使用显式数据类型设置节点值
        # var.get_value()
        # var.set_value(3.9)  # 使用隐式数据类型设置节点值
        # var.get_value()
        tmp = client.get_node("ns=2;i=2")
        # tmp.set_value(ua.Variant(2.3, ua.VariantType.Int32))
        tmp.set_value("aaa")
        print(tmp.get_value())

        uri = "http://examples.freeopcua.github.io"
        idx = client.get_namespace_index(uri)

        # 现在使用其浏览路径获取变量节点
        while True:
            print(root.get_child(["0:Objects"]).get_children())
            myvar = root.get_child(["0:Objects", "{}:MyObject".format(idx), "{}:MyVariable".format(idx)])
            obj = root.get_child(["0:Objects", "2:MyObject"])

            print("myvar is: ", myvar)
            print("myobj is: ", obj)

            myvar.set_value("666")
            # 堆叠myvar访问
            print("myvar is: ", root.get_children()[0].get_children()[1].get_variables()[0].get_value())
            time.sleep(2)

    finally:
        client.disconnect()
