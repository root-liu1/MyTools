import socket
import sys
import threading
import time
from queue import Queue
import getopt
import re
import os

start = time.time()
if os.name == "nt":
    os.system("")

a = "\033[1;34m#################################################################\033[0m"
b = "\033[1;34m#    #######    ####    #####                                   #\033[0m"
c = "\033[1;34m#    #     #  #     #   #    #                                  #\033[0m"
d = "\033[1;34m#    ####### #       #  #    #                                  #\033[0m"
e = "\033[1;34m#    #       #       #  #####                                   #\033[0m"
f = "\033[1;34m#    #        #     #   #    #                                  #\033[0m"
g = "\033[1;34m#    #         ####     #     #           liuhuaiyu@2022.2.1    #\033[0m"
h = "\033[1;34m#################################################################\033[0m"

count = "10"
ip = "127.0.0.1"
port = ""

helpinfo = '''
参考格式：python3 portscan.py [options]
options:
         -h   查看帮助信息
         -v   输出版本
         -u   指定ip
         -p   指定端口
         -t   指定线程数(默认1)

example: python3 portscan.py -u 127.0.0.1 -p 80,445 -t 10
'''


def help_info():
    print(helpinfo)
    sys.exit()


class PortScan(threading.Thread):
    def __init__(self, queue, ip):
        threading.Thread.__init__(self)
        self.queue = queue
        self.ip = ip

    def run(self):
        try:
            while True:
                if self.queue.empty():
                    break
                port = self.queue.get()
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1)
                    result = s.connect_ex((ip, port))
                    if result == 0:
                        print(f"[\033[1;32m*\033[0m] 端口{port}开放")
                    s.close()
                except Exception as e:
                    pass
        except KeyboardInterrupt:
            sys.exit()


def main():
    global ip, queue
    global count
    global port
    threads = []
    thread_count = count
    # 对传入的 port 做处理
    if new != 1:
        queue = Queue()
        if "-" in port:
            port_left = re.search(r"^\d*", port).group()
            port_right = re.search(r"\d*$", port).group()
            for y in range(int(port_left), int(port_right) + 1):
                queue.put(y)
        elif "," in port:
            port_list = re.split(',', port)
            for y in port_list:
                queue.put(int(y))
        else:
            for y in range(65535):
                queue.put(y)
    print(f"[\033[1;32m*\033[0m] 对{ip}进行端口探测")
    print(f"[\033[1;32m*\033[0m] 扫描已开启总计{queue.qsize()}个端口")
    h = input("[\033[1;32m*\033[0m] 端口扫描器初始化已完毕,是否开启扫描(Y/n) ")
    if h == "y" or h == "" or h == "Y":  # 回车键是 ""
        # print("[\033[1;32m*\033[0m] 扫描中...")
        for x in range(int(thread_count)):
            threads.append(PortScan(queue, ip))
        try:
            for i in threads:
                i.start()
            for i in threads:
                i.join()
        except KeyboardInterrupt:
            sys.exit()


if __name__ == '__main__':
    list_logo = [a, b, c, d, e, f, g, h]
    for x in list_logo:
        print(x)
    opts, args = getopt.getopt(sys.argv[1:], "-h,-v,-u:,-p:,-t:")
    for a, b in opts:
        if a == "-h":
            help_info()
        elif a == "-v":
            pass
        elif a == "-u":
            ip = b
        elif a == "-p":
            port = b
            if "," and "-" in port:
                new = 1
                port_list = port.split(',')
                queue = Queue()
                l_list = []
                for x in port_list:
                    if '-' in x:
                        port_left = re.search(r"^\d*", x).group()
                        port_right = re.search(r"\d*$", x).group()
                        for y in range(int(port_left), int(port_right) + 1):
                            l_list.append(y)
                    else:
                        l_list.append(x)
                l_list = set(l_list)
                for l in l_list:
                    queue.put(l)
            else:
                new = 2
        elif a == "-t":
            count = b
    main()
end = time.time()
print(end - start)
