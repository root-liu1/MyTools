import os
import re

a = input("请输入命令: ")


def jiexi(r):
    if r == "help":
        print("这是帮助信息")
    elif r == "show":
        print("这是查看有哪些模块")
    elif "use" in r:
        res = re.search('^use \d', r)

