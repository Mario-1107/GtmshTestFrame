# -*- coding+: utf-8 -*-
"""
@author:Kirito
@file:apiTest.py
@time:2021/07/06
@describe：云POS接口测试
"""
from Comm.tool import Tool
from Config.yamlReader import sys_cfg
from Comm.logger import Logger
import requests,redis


class Apitest():
    # 时间戳
    timestamp = Tool.get_timestamp()
    # 连接本地redis
    conn_redis = redis.Redis(host='localhost', port='6379', db=1)
    # 头部请求不含token
    headers = {
        'Connection': 'keep-alive',
        'retry_count': '1',
        'x-http-timestamp': timestamp,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) electron-react-boilerplate/1.0.0 Chrome/87.0.4280.60 Electron/11.0.1 Safari/537.36',
        'retry': '4',
        'Accept': '*/*',
        'x-http-osversion': '1.0.0',
        'Content-Type': 'application/json',
        'x-http-request-id': '10:08:b1:da:a9:2f-1625563762007',
        'Accept-Language': 'zh-CN',
        'Cookie': 'SERVERID=k8s-ingress.gtmsh.com:10080'
        }

    def __init__(self):
        self.logger = Logger().logger
        # URL前缀
        self.urlPrefix = sys_cfg["api_sit_url"]
        # token
        token = self.login()
        # 头部请求含token
        self.headers_token = {
            'Connection': 'keep-alive',
            'retry_count': '1',
            'x-http-timestamp': self.timestamp,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) electron-react-boilerplate/1.0.0 Chrome/87.0.4280.60 Electron/11.0.1 Safari/537.36',
            'retry': '4',
            'Accept': '*/*',
            'x-http-osversion': '1.0.0',
            'Content-Type': 'application/json; charset=UTF-8',
            'x-http-request-id': '10:08:b1:da:a9:2f-1625563762007',
            'Accept-Language': 'zh-CN',
            'Cookie': 'SERVERID=k8s-ingress.gtmsh.com:10080',
            'x-http-token': token
        }
        # 订单号
        try:
            self.orderNo = self.conn_redis.get('orderNo').decode('utf-8')
            self.logger.info('获取redis订单号成功！orderNo：{}；'.format(self.orderNo))
        except redis.exceptions.ConnectionError as re:
            self.logger.error('连接redis失败，错误：{}；'.format(re))
        # 会员号
        try:
            self.customerId = self.conn_redis.get('customerId').decode('utf-8')
            self.logger.info('获取redis会员号成功！customerId：{}；'.format(self.customerId))
        except redis.exceptions.ConnectionError as re:
            self.logger.error('连接redis失败，错误：{}；'.format(re))
        # 桌号编码
        self.tableCode = '13'


    def login(self,password='12345',shortNo='100008',loginMac='0A:00:27:00:00:16'):
        '''
        获取pos token
        :param password: 密码
        :param shortNo: 账号
        :param loginMac: 设备Mac地址
        :return:token
        '''
        url = self.urlPrefix + "/catering-pos-api/v1/auth/login"
        payload = '{"password":"'+password+'","shortNo":"'+shortNo+'","loginMac":"'+loginMac+'"}'
        response = requests.request("POST", url, headers=self.headers, data=payload)
        code = Tool.get_json_result(response, '$.code')
        if code[0] == 200:
            self.logger.info('登录成功！\n请求参数:{0};\n响应内容：{1}；'.format(payload,response.text))
            token = Tool.get_json_result(response,'$.data.token')
            try:
                #把获取的token存入redis
                self.conn_redis.set('token',token[0])
                self.logger.info('token插入redis成功！插入token为：{}；'.format(token[0]))
                return token[0]
            except:
                self.logger.error('token插入redis失败！')
        else:
            self.logger.error('登录失败！\n请求参数：{0};\n响应内容：{1};\n响应头部:{2};'.format(payload,response.text,response.headers))


    def get_redis_token(self,name='token'):
        '''
        获取redis token
        :param name:redis键名称
        :return:token
        '''
        try:
            token =  self.conn_redis.get(name).decode("utf-8")
            self.logger.info('获取redis，token成功！token：{}；'.format(token))
            return token
        except AttributeError as att:
        # 如果出现错误重新获取token
            self.logger.error("获取token失败，错误信息：{}；".format(att))
            token = self.login()
        except redis.exceptions.ConnectionError as re:
            self.logger.error('连接redis失败，错误：{}；'.format(re))
        return token

    def order_detail(self):
        '''
        台位订单详情
        :return:接口响应内容
        '''
        url = self.urlPrefix + "/catering-pos-api/v1/order/detail"
        payload = '{"orderNo":"'+self.orderNo+'"}'
        response = requests.request("POST", url, headers=self.headers_token, data=payload)
        # 订单菜品唯一编码
        self.orderFoodId = Tool.get_json_result(response,'$.data..orderFoodId')
        self.logger.info('获取台位订单成功！\n请求参数:{0};\n响应内容：{1}；'.format(payload, response.text))
        return  response.text

    def order_summary_canteen_detail(self):
        '''
        堂食正向订单详情
        :return:接口响应内容
        '''
        url = self.urlPrefix + "/catering-pos-api/v1/order/summary/canteen/detail"
        payload = '{"orderNo":"'+self.orderNo+'","customerId":"'+self.customerId+'"}'
        response = requests.request("POST", url, headers=self.headers_token, data=payload)
        self.logger.info('获取堂食正向订单详情成功！\n请求参数:{0};\n响应内容：{1}；'.format(payload, response.text))
        return response.text

    def pay_common_order_pay_detail(self):
        '''
        订单支付详情
        :return:接口响应内容
        '''
        url = self.urlPrefix + "/catering-pos-api/v1/pay/common/order-pay/detail"
        payload = '{"orderNo":"'+self.orderNo+'"}'
        response = requests.request("POST", url, headers=self.headers_token, data=payload)
        self.needPayAmount = str(Tool.get_json_result(response,'$.data.needPayAmount')[0])
        self.logger.info('获取订单支付详情成功！待付金额为：{2}；\n请求参数:{0};\n响应内容：{1}；'.format(payload, response.text,self.needPayAmount))
        return response.text

    def pay_cash_pay(self):
        '''
        现金支付
        :return:接口响应内容
        '''
        url = self.urlPrefix + "/catering-pos-api/v1/pay/cash/pay"
        payload = '{"orderNo":"'+self.orderNo+'","payAmount":"'+self.needPayAmount+'","payModeId":131}'
        response = requests.request("POST", url, headers=self.headers_token, data=payload)
        self.logger.info('现金支付中！支付金额为：{2};\n请求参数:{0};\n响应内容：{1}；'.format(payload, response.text,self.needPayAmount))
        return response.text

    def order_settlement_confirm_checkout(self):
        '''
        确认结账
        :return:接口响应内容
        '''
        url = self.urlPrefix + "/catering-pos-api/v1/order/settlement/confirm-checkout"
        payload = '{"orderNo":"' + self.orderNo + '"}'
        response = requests.request("POST", url, headers=self.headers_token, data=payload)
        vipno = Tool.get_json_result(response,'$.data.cardNo')
        integral = Tool.get_json_result(response,'$.data.totalGiftPoint')
        self.logger.info('结账成功，记得关注会员是否积分！会员号：{2};积分值：{3};\n请求参数:{0};\n响应内容：{1}；'.format(payload, response.text,vipno,integral))
        return response.text

    def order_food_presented(self):
        '''
        菜品赠送
        :return:接口响应内容
        '''
        url = self.urlPrefix + "/catering-pos-api/v1/order/food/presented"
        payload = '{"count":1,"orderItemId":"'+self.orderFoodId[0]+'","orderNo":"'+self.orderNo+'","reason":"大队长礼物","tableCode":"'+self.tableCode+'"}'
        response = requests.request("POST", url, headers=self.headers_token, data=payload.encode('utf-8'))
        self.logger.info('菜品赠送中！\n请求参数:{0};\n响应内容：{1}；'.format(payload, response.text))
        return response.text

    def order_food_cancel_presented(self):
        '''
        取消菜品赠送
        :return:接口响应内容
        '''
        url = self.urlPrefix + "/catering-pos-api/v1/order/food/cancel-presented"
        payload = '{"orderFoodId":"' + self.orderFoodId[0] + '","orderNo":"' + self.orderNo + '","tableCode":"'+self.tableCode+'"}'
        response = requests.request("POST", url, headers=self.headers_token, data=payload.encode('utf-8'))
        self.logger.info('菜品取消赠送！\n请求参数:{0};\n响应内容：{1}；'.format(payload, response.text))
        return response.text

    def order_food_refund(self):
        '''
        菜品退品
        :return: 接口响应内容
        '''
        url = self.urlPrefix + "/catering-pos-api/v1/order/food/refund"
        payload = '{"count":1,"orderItemId":"'+self.orderFoodId[1]+'","orderNo":"'+self.orderNo+'","reason":"承诺三","tableCode":"'+self.tableCode+'"}'
        response = requests.request("POST", url, headers=self.headers_token, data=payload.encode('utf-8'))
        self.logger.info('菜品退品中！\n请求参数:{0};\n响应内容：{1}；'.format(payload, response.text))
        return response.text

    def order_food_cancel_refund(self):
        '''
        取消退品
        :return:接口响应内容
        '''
        url = self.urlPrefix + "/catering-pos-api/v1/order/food/cancel-refund"
        payload = '{"orderFoodId":"'+self.orderFoodId[1]+'","orderNo":"'+self.orderNo+'","tableCode":"'+self.tableCode+'"}}'
        response = requests.request("POST", url, headers=self.headers_token, data=payload.encode('utf-8'))
        self.logger.info('退品取消中！\n请求参数:{0};\n响应内容：{1}；'.format(payload, response.text))
        return response.text

    def order_change_people(self):
        '''
        修改台位人数
        :return:接口响应内容
        '''
        url = self.urlPrefix + "/catering-pos-api/v1/order/change/people"
        payload = '{"tableCode":"'+self.tableCode+'","peopleNum":"8","orderNo":"'+self.orderNo+'"}'
        response = requests.request("POST", url, headers=self.headers_token, data=payload.encode('utf-8'))
        self.logger.info('修改台位人数中！\n请求参数:{0};\n响应内容：{1}；'.format(payload, response.text))
        return response.text

    def order_vip_bind(self):
        '''
        会员绑定
        :return:接口响应内容
        '''
        url = self.urlPrefix + "/catering-pos-api/v1/order/vip/bind"
        payload = '{"cardNo":"660000000151","customerId":1000348986,"orderNo":"'+self.orderNo+'","tableCode":"'+self.tableCode+'"}'
        response = requests.request("POST", url, headers=self.headers_token, data=payload.encode('utf-8'))
        self.logger.info('会员绑定中！\n请求参数:{0};\n响应内容：{1}；'.format(payload, response.text))
        return response.text

    def table_open(self):
        '''
        开台
        :return:接口响应内容
        '''
        url = self.urlPrefix + "/catering-pos-api/v1/table/open"
        payload = '{"tableCode":"'+self.tableCode+'","peopleNum":"5","teaCode":"F1000009805"}'
        response = requests.request("POST", url, headers=self.headers_token, data=payload.encode('utf-8'))
        self.orderNo = Tool.get_json_result(response,'$.data.orderNo')[0]
        self.logger.info('台位开台中！\n请求参数:{0};\n响应内容：{1}；'.format(payload, response.text))
        try:
            self.conn_redis.set('orderNo',self.orderNo)
            self.logger.info('订单号插入redis成功！插入订单号为：{};'.format(self.orderNo))
        except:
            self.logger.error('订单号插入redis失败')
        return response.text

    def table_repeal(self):
        '''
        退台
        :return:接口响应内容
        '''
        url = self.urlPrefix + "/catering-pos-api/v1/table/repeal"
        payload = '{"reasonCode":"back-01","tableCode":"' + self.tableCode + '"}'
        response = requests.request("POST", url, headers=self.headers_token, data=payload.encode('utf-8'))
        self.logger.info('台位退台中！\n请求参数:{0};\n响应内容：{1}；'.format(payload, response.text))
        return response.text

    def order_submit(self):
        '''
        下单
        :return:接口响应内容
        '''
        url = self.urlPrefix + "/catering-pos-api/v1/order/submit"
        payload = '{"orderNo":"'+self.orderNo+'","submitItemList":[{"fixingsGroupFoodList":[],"foodCode":"F1000009742","foodMadeList":[{"madeCode":"502","madeName":"免薄荷叶","madeType":"08","raisePrice":"0.00","subjectMadeKey":"350_502"}],"foodNum":3,"foodType":1,"mealFoodList":[]},{"fixingsGroupFoodList":[],"foodCode":"F1000017977","foodMadeList":[],"foodNum":1,"foodType":1,"mealFoodList":[]}],"tableCode":"'+self.tableCode+'","tableName":"'+self.tableCode+'"}'
        response = requests.request("POST", url, headers=self.headers_token, data=payload.encode('utf-8'))
        self.logger.info('订单提交中！\n请求参数:{0};\n响应内容：{1}；'.format(payload, response.text))
        return response.text

    def test_1(self):
        '''
        台位有订单结台
        :return:
        '''
        self.order_detail()#订单详情
        self.pay_common_order_pay_detail()#订单支付详情
        self.pay_cash_pay()#现金支付
        self.order_settlement_confirm_checkout()#结台

    def test_2(self):
        '''
        pos开台并结账
        :return:
        '''
        self.table_open()  # pos开台
        self.order_detail()  # 订单详情
        self.order_submit()  # 提交订单
        self.order_vip_bind() #绑定会员
        self.pay_common_order_pay_detail()  # 订单支付详情
        self.pay_cash_pay()  # 现金支付
        self.order_settlement_confirm_checkout()  # 结台

if __name__ == '__main__':
    test = Apitest()
    test.test_1()
