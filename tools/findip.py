import getopt
import time
from queue import Queue
import sys
import threading
import subprocess

start = time.time()

url = ""
thread = "1"
new_url = ""
threads = []

helpinfo = '''
参考格式：python3 dirscan.py [options]
options:
         -h   查看帮助信息
         -v   输出版本
         -u   指定url
         -t   指定线程数(默认1)

example: python3 findip.py -u 127.0.0.1 -t 10
'''


def help():
    print(helpinfo)
    sys.exit()


class FindThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            if self.queue.empty():
                break
            fip = self.queue.get()
            # 这里写检测ip是否存活
            try:
                result = subprocess.Popen(f'ping -n 1 {fip}', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE, encoding='gbk')
                res = result.stdout.read()
                if "TLL" and "时间" in res:
                    print(f"{fip} is up")
                    write_ip(fip=fip)
                else:
                    # print(f"{fip} is down")
                    pass
            except:
                print(f"探测IP{fip}出错")


def write_ip(fip):
    with open('up_ip.txt', "a", encoding='utf-8') as f:
        f.write(fip)
        f.write("\n")


def main():
    global new_url
    queue = Queue()
    a = len(url.split('.')[-1])
    if a == 1:
        new_url = url[:-1]
        print(new_url)
    elif a == 2:
        new_url = url[:-2]
        print(new_url)
    elif a == 3:
        new_url = url[:-3]
        print(new_url)
    else:
        print("格式有错误")
        sys.exit()
    for x in range(1, 255):
        queue.put(new_url + str(x))
    for i in range(int(thread)):
        threads.append(FindThread(queue=queue))
    for y in threads:
        y.start()
    for y in threads:
        y.join()


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "-u:,-t:,-h")
    for a, b in opts:
        if a == "-u":
            url = b
            continue
        elif a == "-t":
            thread = b
            continue
        elif a == "-h":
            help()
    main()
    end = time.time()
    print(end - start)
