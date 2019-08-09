from opcua import ua, Server
import random
import time


def subscribe():
    server = Server()
    server.set_endpoint("opc.tcp://192.168.21.36:4840")

    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)

    objects = server.get_objects_node()

    myobj = objects.add_object(idx, "MyObject")

    myvar = myobj.add_variable(idx, "MyVariable", 6.6)
    myvar.set_writable()

    mysub = myobj.add_variable(idx, "Alarm", 0)

    server.start()
    while True:
        data = random.random()
        if data > 0.5:
            mysub.set_value(data)
        time.sleep(0.1)

    # server.stop()


if __name__ == "__main__":
    subscribe()
