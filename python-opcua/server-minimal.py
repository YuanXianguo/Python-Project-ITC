import sys
sys.path.insert(0, "..")

import time

from opcua import ua, Server

if __name__ == "__main__":
    # setup our server
    server = Server()
    server.set_endpoint("opc.tcp://192.168.21.36:4840")

    # 设置我们自己的命名空间，不是必要的，但应该作为规范
    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)

    # 获取对象节点，这是我们应该放置节点的地方
    objects = server.get_objects_node()
    print(objects.get_children())

    # 填充我们的地址空间
    myobj = objects.add_object(idx, "MyObject")
    print(myobj)
    print(objects.get_children())

    myvar = myobj.add_variable(idx, "MyVariable", 6.7)
    print(myvar)
    print(objects.get_children())

    myvar.set_writable()    # 将MyVariable设置为可由客户端写入

    # starting!
    server.start()

    try:
        count = 0
        while True:
            time.sleep(1)
            count += 0.1
            myvar.set_value(count)
    finally:
        # close connection, remove subcsriptions, etc
        server.stop()

