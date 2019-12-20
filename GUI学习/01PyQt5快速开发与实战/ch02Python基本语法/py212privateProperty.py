class MyCounter():
    __secret_count = 0 #私有变量
    public_count = 0 #公共变量
    def __private_count_fun(self):
        print("这是私有方法")
        self.__secret_count += 1
        self.public_count += 1
        print("self.__secret_count={}".format(self.__secret_count))

    def public_count_fun(self):
        print("这是公共方法")
        self.__private_count_fun()

if __name__ == '__main__':
    counter = MyCounter()
    counter.public_count_fun()
    counter.public_count_fun()

    print("instance public_count={}".format(counter.public_count))
    print("class public_count={}".format(MyCounter.public_count))

if __name__ == '__main__':
    counter = MyCounter()
    print(counter.__secret_count) # 实例不能访问私有变量
    counter.__private_count_fun() # 实例不能访问私有方法

