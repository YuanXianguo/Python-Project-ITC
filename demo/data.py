import random
import time
# random.uniform(50, 100), random.randint(5000, 7000),0, random.uniform(10, 50)
data1 = list()
data2 = list()
data3 = list()
t = list()
for i in range(10):
    data1.append(str(round(random.uniform(50, 100), 2)))
    data2.append(str(random.randint(5000, 7000)))
    data3.append(str(round(random.uniform(10, 50), 2)))
    t.append("'{}'".format(time.strftime("%H:%M:%S", time.localtime())))
    time.sleep(0.5)
with open("data1.txt", "w") as f:
    f.write(",".join(data1))
with open("data2.txt", "w") as f:
    f.write(",".join(data2))
with open("data3.txt", "w") as f:
    f.write(",".join(data3))
with open("t.txt", "w") as f:
    f.write(",".join(t))
