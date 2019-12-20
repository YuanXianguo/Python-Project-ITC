import numpy as np
import time,sys

def test():
    a = np.arange(400000).reshape(100, 100, 20, 2)
    start = time.perf_counter()
    a.tofile('test.dat', sep=',', format='%d')
    mid = time.perf_counter()
    b = np.fromfile('test.dat', dtype=np.int, sep=',').reshape(100, 100, 20, 2)
    c = b[0].reshape(2000, 2)
    b[0] = c.reshape(100, 20, 2)
    b.tofile('test4.dat')
    d = np.fromfile('test4.dat')
    print(d)
    print(c.nbytes)
    end = time.perf_counter()
    print('存储：{}s'.format(mid-start), '读取：{}s'.format(end-mid), '总：{}s'.format(end-start))

def test1():
    a = np.ones((100, 100, 20, 2))
    start = time.perf_counter()
    a.tofile('test1.dat')
    mid = time.perf_counter()
    b = np.fromfile('test1.dat').reshape(100, 100, 20, 2)
    end = time.perf_counter()
    print('存储：{}s'.format(mid-start), '读取：{}s'.format(end-mid), '总：{}s'.format(end-start))

def test2():
    a = np.ones((100, 100, 20, 2))
    a[0][0][0][0:2] = 2
    start = time.perf_counter()
    np.save('test3.npy', a)
    mid = time.perf_counter()
    b = np.load('test3.npy')
    end = time.perf_counter()
    print('存储：{}s'.format(mid-start), '读取：{}s'.format(end-mid), '总：{}s'.format(end-start))
    print(a)

def test3():
    list = [1,1]
    list[0] = 2
    print(list)

def test4():
    a = np.ones((100, 100, 20, 2))
    a.tofile('test1.dat')
    a[0][0][0][0:2] = 2
    print(a)
    b = np.fromfile('test1.dat').reshape((100, 100, 20, 2))
    print(b)

test3()
