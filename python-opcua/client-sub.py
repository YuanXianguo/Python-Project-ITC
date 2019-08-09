from opcua import Client,ua
import threading
import time


class SubHandler():
    def datachange_notification(self, node, val, data):
        print(node, val)


def subscribe(client, mysub):
    handler = SubHandler()
    sub = client.create_subscription(100, handler)
    sub.subscribe_data_change(mysub)


def main(myvar, mysub):

    while True:
        print(myvar.get_value(), mysub.get_value())
        # time.sleep(0.1)

    # client.disconnect()


if __name__ == "__main__":
    client = Client("opc.tcp://192.168.21.36:4840")
    client.connect()

    root = client.get_root_node()

    uri = "http://examples.freeopcua.github.io"
    idx = client.get_namespace_index(uri)

    myvar = root.get_child(["0:Objects", "{}:MyObject".format(idx), "{}:MyVariable".format(idx)])
    mysub = root.get_child(["0:Objects", "{}:MyObject".format(idx), "{}:Alarm".format(idx)])

    subscribe(client, mysub)
    main(myvar, mysub)
    # p1 = threading.Thread(target=subscribe, args=(client, mysub))
    # p1.start()
    # p2 = threading.Thread(target=main, args=(myvar, mysub))
    # p2.start()
