import os
import sys
import time
import subprocess

if os.name == "nt":
    os.system("")
wait_show_head = '{*\033[1;32m等待登录\033[0m*} '
wrong_show_head = '{*\033[1;31m ❌-❌-❌ \033[0m*} '
success_show_head = '{*\033[1;35m已登录\033[0m*} '
print(wait_show_head + "欢迎来到MyTool渗透工具包!")
try:
    from key_code import suiji

    token_sum = suiji(20)
    with open("key.txt", "w", encoding='utf-8') as f:
        f.write(token_sum)
except:
    print(wrong_show_head + "出现未知错误!")
    sys.exit()
if os.path.exists('./key.txt'):
    list_num = [3, 2, 1, 0]
    for x in list_num:
        print("许可证已经下发,文件名为key.txt")
        key_one = input("请输入许可密钥: ")
        if x == 0:
            if key_one != token_sum:
                print(wrong_show_head + "你已经没有机会了，再见!")
                sys.exit()
        if key_one != token_sum:
            print(wrong_show_head + f"许可证错误! 你还有{x}次机会")
        else:
            print("密钥正确!")
            break
else:
    print(wrong_show_head + "未检测到密钥文件，请检查!")
    sys.exit()
account = input("请输入许可用户: ")
accounts = []
with open('account.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        accounts.append(line.strip())
if account.strip() not in accounts:
    print(wrong_show_head + "你不是许可人物,不可以登录,滚😠!!!")
    sys.exit()
else:
    if account != "liu":
        user_show_head = f'[*\033[1;34m{account}\033[0m*]'
    else:
        user_show_head = '{*\033[1;35m@Liu~神\033[0m*}'
print(user_show_head + f"您已成功登录,欢迎{account}使用本工具!")
print(user_show_head + "本工具目前集成了以下几个模块: ")
option = []
dic = {}
# 通过死循环遍历tools目录下的脚本，并输出，存入字典，根据标号可以选择出文件名，进行快速执行
while True:
    for x in os.listdir(r"D:\Pycharm\pycharmHome\MyTool\tools"):
        print([os.listdir(r'D:\Pycharm\pycharmHome\MyTool\tools').index(x)], end=' ')
        print(x)
        dic.setdefault(os.listdir(r'D:\Pycharm\pycharmHome\MyTool\tools').index(x), x)
    while True:
        try:
            result = input(user_show_head + "请选择你要运行的模块: ")
            if result == "exit":
                print(user_show_head + "\033[1;32m谢谢使用,再见\033[0m")
                sys.exit()  # 这里的退出属于返回异常，所以要跳到 except 中
            if result == "":
                continue
            if int(result) < 0 or int(result) >= len(os.listdir(r"D:\Pycharm\pycharmHome\MyTool\tools")):
                print(wrong_show_head + "选项不正确，请重新输入!")
                for x in dic:
                    print([x], end=" ")
                    print(dic[x])
            else:
                print(user_show_head + f"你选择的是{dic[int(result)]}脚本")
                break
        except SystemExit as e:
            sys.exit()  # 捕获退出异常
        except KeyboardInterrupt as e:
            print("发送CTRL+C退出")
            sys.exit()
        except:
            print(wrong_show_head + "选项不正确，请重新输入!")
            for x in dic:
                print([x], end=" ")
                print(dic[x])
    print(user_show_head + "脚本信息如下")
    time.sleep(0.5)
    os.system(fr'python3 D:\Pycharm\pycharmHome\MyTool\tools\{dic[int(result)]} -h')
    if "tools" not in os.getcwd():
        os.chdir('./tools')
    while True:
        a = input(user_show_head + "请配置参数: ")
        if a == "exit":
            print(user_show_head + "\033[1;31m回退\033[0m")
            break
        elif a == "":
            continue
        elif a == "show":
            os.system(fr'python3 D:\Pycharm\pycharmHome\MyTool\tools\{dic[int(result)]} -h')
        else:
            try:
                res = subprocess.run(a, shell=True, encoding='gbk')
            except:
                print(user_show_head + "参数配置有误")
