import random
from itertools import count  # 无限大


# 生成max位随机数,用作工具登陆的密钥
def suiji(max):
    str = ''
    suiji_str = 'abcdefghigklmnopqrstuvwxyzabcdefghigklmnopqrstuvwxyzABCDEFGHIGKLMNOPQRSTUVWXYZABCDEFGHIGKLMNOPQRSTUVWXYZ0123456789'
    leng = len(suiji_str) - 1
    for x in count():
        str1 = suiji_str[random.randint(0, leng)]
        if x >= 5:
            if str[len(str) - 2:].isalpha() and str1.isalpha():  # 判断字符串最后两位和新随即出来的数的类型是否相同，如过相同跳出本循环，开始下一次循环
                continue
        str += str1
        if len(str) == max:
            return str
