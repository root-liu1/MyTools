import linecache
import os
import random
import sys
import threading
import time
import chardet
import requests
from queue import Queue
import getopt

st = time.time()
if os.name == "nt":
    os.system("")

a = "\033[1;34m#################################################################\033[0m"
b = "\033[1;34m#    #####       #     #####                                    #\033[0m"
c = "\033[1;34m#    #     #     #     #    #                                   #\033[0m"
d = "\033[1;34m#    #     #     #     #    #                                   #\033[0m"
e = "\033[1;34m#    #     #     #     #####                                    #\033[0m"
f = "\033[1;34m#    #     #     #     #    #                                   #\033[0m"
g = "\033[1;34m#    #####       #     #     #           liuhuaiyu@2022.2.1     #\033[0m"
h = "\033[1;34m#################################################################\033[0m"

url = "http://127.0.0.1"
thread = "1"
dic = "dir.txt"
status = []
write_path = "new_dir_result.txt"
version = '''
当前版本：v1.0.0
'''
helpinfo = '''
参考格式：python3 dirscan.py [options]
options:
         -h   查看帮助信息
         -v   输出版本
         -u   指定url
         -d   指定字典文件(默认dir.txt)
         -t   指定线程数(默认1)
         -o(可选)   指定输出的状态码(默认为200)
         -w(可选)   指定保存文件名(默认保存在当前目录下new_dir_result.txt)
         
example: python3 dirscan.py -u http://127.0.0.1/ -d dir.txt -t 10
'''


def help_info():
    print(helpinfo)
    sys.exit()


def version_info():
    print(version)
    sys.exit()


def random_ua():
    count_ran = random.randint(1, 497)
    return linecache.getline("1.txt", count_ran)


def set_encode(file):
    try:
        with open(file, 'rb') as f:
            fp = f.read()
            result = chardet.detect(fp)
            return result['encoding']
    except:
        print("[\033[1;31m!\033[0m] 字典自动设置编码失败!")
        sys.exit()


class MyScan(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            if self.queue.empty():
                break
            url_path = self.queue.get()
            headers = {
                "User-Agent": random_ua().strip()
            }
            try:
                response = requests.get(url=url_path, headers=headers)  # 添加 allow_redirects=False 会导致301跳转页面扫不出来
                result = f"[\033[1;32m+\033[0m]状态码:[\033[1;33m{response.status_code}\033[0m]---目标大小:[{len(response.text)}]---目标地址:{url_path}"
                if status:
                    if response.status_code in status:
                        print(result)
                else:
                    if response.status_code == 200:
                        print(result)
                if response.status_code == 200:
                    write_result(url=url_path)
            except Exception as e:
                print("在第" + str(e.__traceback__.tb_lineno) + "出错")
                print(f"\033[1;31m{e}\033[0m")


def write_result(url):
    with open(write_path, "a", encoding='utf-8') as f:
        f.write(url)
        f.write("\n")


def go():
    global url
    queue = Queue()
    if "://" not in url:
        print("[\033[1;31m!\033[0m] 请在url中添加http或https")
        sys.exit()
    if url.endswith("/"):
        url = url.rstrip("/")  # 只有要对全局变量修改时候才用 global 引入
    print(f"[\033[1;32m*\033[0m] 加载字典: {dic}")
    with open(dic, 'r', encoding=set_encode(file=dic)) as f:
        for i in f.readlines():
            queue.put(url + i.strip())
    print(f"[\033[1;32m*\033[0m] 字典加载完毕")
    print(f"[\033[1;32m*\033[0m] 总计{queue.qsize()}行")
    print(f"[\033[1;32m*\033[0m] 目标地址: {url}")
    print(f"[\033[1;32m*\033[0m] 您设置的线程数: {thread}")
    if "-o" in sys.argv[1:]:
        print(f"[\033[1;32m*\033[0m] 您设置的输出状态码为{status}")
    print(f"[\033[1;32m*\033[0m] 您设置的保存文件名为{write_path}")
    try:
        if os.stat(write_path).st_size != 0:
            rr = input("[\033[1;32m*\033[0m] 检测到文件已有内容,是否清空文件(Y/n) ")
            if rr == "" or rr == "Y":
                with open(write_path, "w", encoding='utf-8') as ff:
                    ff.write("")
                print("[\033[1;32m*\033[0m] 文件已经清空")
        else:
            pass
    except FileNotFoundError:
        pass
    h = input("[\033[1;32m*\033[0m] 目录扫描器初始化已完毕,是否开启扫描(Y/n) ")
    if h == "y" or h == "" or h == "Y":  # 回车键是 ""
        print("[\033[1;32m*\033[0m] 扫描中...")
        threads = []
        for x in range(int(thread)):
            threads.append(MyScan(queue))
        for i in threads:
            i.start()
        for i in threads:
            i.join()
    elif h == "n":
        print("[\033[1;32m!\033[0m] 程序已退出")
        sys.exit()
    else:
        print("[\033[1;31m!\033[0m] 请输入正确选项")
        sys.exit()


if __name__ == '__main__':
    list_logo = [a, b, c, d, e, f, g, h]
    for x in list_logo:
        print(x)
    if len(sys.argv[1:]) < 1 or len(sys.argv[1:]) > 10:
        help_info()
    opts, args = getopt.getopt(sys.argv[1:], "-h,-v,-u:,-d:,-t:,-o:,-w:")
    for a, b in opts:
        if a == "-t":
            if int(b) < 1:
                b = 1
            thread = b
            continue
        elif a == "-u":
            url = b
            continue
        elif a == "-d":
            dic = b
            continue
        elif a == "-o":
            for x in b.split(","):
                status.append(int(x))
            continue
        elif a == "-w":
            write_path = b
            continue
        elif a == "-h":
            help_info()
        elif a == "-v":
            version_info()
    go()
    end = time.time()
    print("程序已结束共耗时: " + str(end - st))
