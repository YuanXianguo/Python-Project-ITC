import psutil,time,os
print(psutil.disk_partitions()[-1],psutil.disk_partitions()[-1][-1])
if 'removable' in psutil.disk_partitions()[-1][-1]:
    print(psutil.disk_partitions()[-1][0])
    w_path = psutil.disk_partitions()[-1][0]
    file_name = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime())
    path = os.path.join(w_path, file_name)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('python')
        f.close()

