# -*- coding+: utf-8 -*-
"""
@author:Kirito
@file:tool.py
@time:2021/06/18
@describe：工具类
"""
import random, string,time,json,jsonpath


class Tool():

    @staticmethod
    def get_randoms(length=32):
        '''
        生成指定位数随机数
        :param length:长度,默认32位
        :return:返回随机数
        '''
        randoms = ''.join(random.sample(string.digits + string.ascii_letters, length))
        return randoms

    @staticmethod
    def get_json_result(response, value):
        '''
        提取JSON的部分内容
        :param response:内容
        :param value:提取操作符
        :return:提取内容
        '''
        # 先把传入的值转换为json格式
        responses = json.loads(response.content)
        # 将需要提取的值提取出来
        result = jsonpath.jsonpath(responses, "%s" % value)
        return result

    @staticmethod
    def get_orderno():
        '''
        生成当前时间戳订单号
        :return:订单号
        '''
        orderno = str(int((time.time() * 1000)))
        return orderno

    @staticmethod
    def get_phone_number(key=False):
        '''
        生成随机电话号码
        :param key:默认生成虚假手机号，True 生成真实手机号
        :return:随机手机号
        '''
        pre_list = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139",
                    "147", "150", "151", "152", "153", "155", "156", "157", "158", "159",
                    "186", "187", "188", "189"]
        if key:
            result = random.choice(pre_list) + ''.join(random.choice("0123456789") for i in range(8))
        else:
            result = random.choice(pre_list) + ''.join(random.choice('0123456789') * 4) + ''.join(
                random.choice('0123456789') * 4)
        return result

    @staticmethod
    def get_email():
        '''
        生成随机邮箱号
        :return:随机邮箱
        '''
        # 邮箱后缀
        email_str = ''
        email_suffix = ['@163.com', '@qq.com', '@gtmsh.com']
        # 用数字0-9 和字母a-z 生成随机邮箱
        list_sum = [i for i in range(10)] + ["a", "b", "c", "d", "e", "f", "g", "h", 'i', "j", "k",
                                             "l", "M", "n", "o", "p", "q", "r", "s", "t", "u", "v",
                                             "w", "x", "y", "z"]
        for i in range(10):
            a = str(random.choice(list_sum))
            email_str = email_str + a
        # 随机拼接不同的邮箱后缀
        return email_str + random.choice(email_suffix)

    @staticmethod
    def get_timestamp():
        '''
        生成当前时间的时间戳
        :return:
        '''
        timestamp = str(int((time.time() * 1000)))
        return timestamp


if __name__ == '__main__':
    c = Tool.get_timestamp()
    print(len(c))
