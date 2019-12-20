class MyClass():
    count = 0
    name = 'DefaultName'
    def __init__(self, name):
        self.name = name
        print("类的变量是{}\n对象的变量是{}".format(MyClass.name, self.name))

    def set_count(self, count):
        self.count = count

    def get_count(self):
        return self.count

if __name__ == '__main__':
    cls = MyClass('lisi')
    cls.set_count(10)
    print('count={}'.format(cls.get_count()))
