import sys
sys.path.insert(0, "..")
import logging
import time

try:
    from IPython import embed
except ImportError:
    import code

    def embed():
        vars = globals()
        vars.update(locals())
        shell = code.InteractiveConsole(vars)
        shell.interact()


from opcua import Client
from opcua import ua


class SubHandler(object):

    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another
    thread if you need to do such a thing
    订阅处理程序。 从服务器接收订阅的事件
  data_change和event方法直接从接收线程调用。
  不要在那里做昂贵，缓慢或网络操作。 创建另一个线程，如果你需要做这样的事情
    """

    def datachange_notification(self, node, val, data):
        print("Python: New data change event", node, val)

    def event_notification(self, event):
        print("Python: New event", event)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)
    # logger = logging.getLogger("KeepAlive")
    # logger.setLevel(logging.DEBUG)

    client = Client("opc.tcp://localhost:502/")
    # client = Client("opc.tcp://admin@localhost:4840/freeopcua/server/") #connect using a user
    try:
        client.connect()
        client.load_type_definitions()  # 加载服务器特定结构/扩展对象的定义

        # 客户端有一些方法可以获取UA节点的代理，这些节点应始终位于地址空间中，例如Root或Objects
        root = client.get_root_node()
        print("Root node is: ", root)
        objects = client.get_objects_node()
        print("Objects node is: ", objects)

        # Node objects have methods to read and write node attributes as well as browse or populate address space
        print("Children of root are: ", root.get_children())
        for node in root.get_children():
            print(node.get_children())
        print("Children of objects are: ", objects.get_children())
        for node in objects.get_children():
            print(node.get_children())
        # get a specific node knowing its node id
        #var = client.get_node(ua.NodeId(1002, 2))
        #var = client.get_node("ns=3;i=2002")
        #print(var)
        #var.get_data_value() # get value of node as a DataValue object
        #var.get_value() # get value of node as a python builtin
        #var.set_value(ua.Variant([23], ua.VariantType.Int64)) #set node value using explicit data type
        #var.set_value(3.9) # set node value using implicit data type

        # gettting our namespace idx
        uri = "http://examples.freeopcua.github.io"
        idx = client.get_namespace_index(uri)
        print(idx)
        # Now getting a variable node using its browse path
        myvar = root.get_child(["0:Objects", "{}:MyObject".format(idx), "{}:MyVariable".format(idx)])
        myarrayvar = root.get_child(["0:Objects", "{}:MyObject".format(idx), "{}:myarrayvar".format(idx)])
        print("myarrayvar:", myarrayvar.get_children())

        print("myarrayvar:", myarrayvar.get_value())
        obj = root.get_child(["0:Objects", "{}:MyObject".format(idx)])
        print("myvar is: ", myvar)
        print("obj:",obj)

        # 订阅变量节点
        handler = SubHandler()
        sub = client.create_subscription(500, handler)
        handle = sub.subscribe_data_change(myvar)
        time.sleep(0.1)

        # 我们也可以从服务器订阅事件
        sub.subscribe_events()
        # sub.unsubscribe(handle)
        # sub.delete()

        # 在服务器上调用方法
        res = obj.call_method("{}:multiply".format(idx), 3, "klk")
        print("method result is: ", res)

        embed()
    finally:
        client.disconnect()
