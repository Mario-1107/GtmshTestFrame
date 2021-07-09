# -*- coding+: utf-8 -*-
"""
@author:Kirito
@file:order_api_test.py
@time:2021/07/07
@describe：订单相关API
"""
from Comm.logger import Logger
from Comm.tool import Tool
from Config.yamlReader import sys_cfg
import requests,redis


class Order_Api_Test():
    # 当前13位时间戳
    timestamp = Tool.get_timestamp()
    # 连接本地redis
    conn_redis = redis.Redis(host='localhost', port='6379', db=1)

    def __init__(self, token):
        '''
        构造函数
        :param token: 接口操作token
        '''
        self.logger = Logger().logger
        self.token = token
        self.headers = {
            'Connection': 'keep-alive',
            'x-http-token': self.token,
            'x-http-timestamp': self.timestamp,
            'x-http-devicetype': 'WechatMiniProgram',
            'x-http-channel': '5',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1 wechatdevtools/1.05.2106250 MicroMessenger/8.0.5 Language/zh_CN webview/',
            'x-http-version': '3.9.17',
            'content-type': 'application/json',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://servicewechat.com/wxdb833922e5e14593/devtools/page-frame.html',
            'Content-Type': 'application/json'
        }
        # 品牌编码
        self.brandCode = '823885'
        # 门店编码
        self.shopCode = '8999'
        # 桌号编码
        self.tableCode = '13'
        # 用餐人数
        self.peopleNum = '3'
        # 订单号
        # try:
        #     self.orderNo = self.conn_redis.get('orderNo').decode('utf-8')
        #     self.logger.info('获取redis订单号成功！orderNo：{}'.format(self.orderNo))
        # except redis.exceptions.ConnectionError as re:
        #     self.logger.error('连接redis失败，错误：{}'.format(re))

    def cart_check_binding_table(self, latitude='22.50663', longitude='113.94088'):
        '''
        购物车绑定品牌、门店、桌号
        :param latitude:用户纬度
        :param longitude:用户经度
        :param brandCode:品牌编码
        :param shopCode:门店编码
        :param tableCode:桌号编码
        :return:接口响应内容
        '''
        url = sys_cfg["api_sit_url"] + '/dianxin-mp/v1/v2/cart/check-binding-table'
        payload = '{"latitude":"' + latitude + '","longitude":"' + longitude + '","brandCode":"' + self.brandCode + '","cartOrderType":1,"shopCode":"' + self.shopCode + '","tableCode":"' + self.tableCode + '","tableName":"' + self.tableCode + '","businessType":1}'
        response = requests.request("POST", url, headers=self.headers, data=payload)
        self.logger.info('进入{2}台位成功！\n请求参数:{0};\n响应内容：{1}'.format(payload, response.text, self.tableCode))
        return response.text

    def save_people_number(self):
        '''
        用餐人数和茶水类型
        :return:接口响应内容
        '''
        url = sys_cfg["api_sit_url"] + '/dianxin-mp/v1/v2/cart/save-people-number'
        payload = '{"businessType":1,"savePage":true,"brandCode":"' + self.brandCode + '","cartOrderType":1,"shopCode":"' + self.shopCode + '","tableCode":"' + self.tableCode + '","tableName":"' + self.tableCode + '","peopleNum":"' + self.peopleNum + '","teaWaterRequest":{"foodCode":"F1000009771","foodNum":1}}'
        response = requests.request("POST", url, headers=self.headers, data=payload)
        self.logger.info('保存茶位人数成功！\n请求参数:{0};\n响应内容：{1}'.format(payload, response.text))
        return response.text

    def cart_add(self):
        '''
        添加菜品
        :return:接口响应内容
        '''
        url = sys_cfg["api_sit_url"] + '/dianxin-mp/v1/v2/cart/add'
        # 单品
        payload = '{"businessType":1,"brandCode":"' + self.brandCode + '","cartOrderType":1,"shopCode":"' + self.shopCode + '","tableCode":"' + self.tableCode + '","tableName":"' + self.tableCode + '","foodCategoryCode":"F1000029630","foodCode":"F1000009791","foodNum":1}'
        # 套餐
        payload2 = '{"businessType":1,"brandCode":"' + self.brandCode + '","cartOrderType":1,"shopCode":"' + self.shopCode + '","tableCode":"' + self.tableCode + '","tableName":"' + self.tableCode + '","foodCategoryCode":"F1000045467","foodCode":"F1000045463","setMealFoodRequests":[{"foodNum":1,"foodCode":"F1000009742","optional":1,"subjectItemKey":"4869_F1000009742"},{"foodNum":1,"foodCode":"F1000009788","optional":1,"subjectItemKey":"4869_F1000009788"},{"foodNum":1,"foodCode":"F1000009738","optional":1,"subjectItemKey":"4869_F1000009738"},{"foodNum":1,"foodCode":"F1000009846","optional":1,"subjectItemKey":"4869_F1000009846"}],"foodNum":1}'
        # 做法商品
        payload3 = '{"businessType":1,"brandCode":"' + self.brandCode + '","cartOrderType":1,"shopCode":"' + self.shopCode + '","tableCode":"' + self.tableCode + '","tableName":"' + self.tableCode + '","foodCategoryCode":"F1000017272","foodCode":"F1000009888","foodNum":1,"madeRequests":[{"madeName":"少冰别名","subjectMadeKey":"473_506"}]}'
        response = requests.request("POST", url, headers=self.headers, data=payload)
        self.logger.info('单品加入购物车成功！\n请求参数:{0};\n响应内容：{1}'.format(payload, response.text))
        response2 = requests.request("POST", url, headers=self.headers, data=payload2.encode("utf-8"))
        self.logger.info('套餐加入购物车成功！\n请求参数:{0};\n响应内容：{1}'.format(payload2, response2.text))
        response3 = requests.request("POST", url, headers=self.headers, data=payload3.encode("utf-8"))
        self.logger.info('含做法商品加入购物车成功！\n请求参数:{0};\n响应内容：{1}'.format(payload3, response3.text))
        return response.text, response2.text, response3.text

    def sale_order_submit(self):
        '''
        提交订单
        :return:接口响应内容
        '''
        url = sys_cfg["api_sit_url"] + "/dianxin-mp/v1/v2/sale-order/submit"
        payload = '{"cartOrderType":1,"shopCode":"'+self.shopCode+'","tableCode":"'+self.tableCode+'"}'
        response = requests.request("POST", url, headers=self.headers, data=payload)
        self.orderNo = Tool.get_json_result(response, '$.data.orderNo')[0]
        self.logger.info('下单成功，订单号为:{2};\n请求参数:{0};\n响应内容：{1}'.format(payload, response.text, self.orderNo))
        try:
            self.conn_redis.set('orderNo',self.orderNo)
            self.logger.info('订单号插入redis成功！插入订单号为：{};'.format(self.orderNo))
        except:
            self.logger.error('订单号插入redis失败')
        return response.text

    def sale_order_detail(self):
        '''
        订单详情
        :return:接口响应内容
        '''
        url = sys_cfg["api_sit_url"] + '/dianxin-mp/v1/v2/sale-order/detail'
        payload = '{"orderNo":"'+self.orderNo+'","orderSource":"local"}'
        response = requests.request("POST", url, headers=self.headers, data=payload)
        self.logger.info('获取订单详情成功！\n请求参数:{0};\n响应内容：{1}'.format(payload, response.text))
        return response.text

    def shop_table_check(self):
        '''
        门店台位订单检查
        :return:接口响应内容
        '''
        url = sys_cfg["api_sit_url"] + '/dianxin-mp/v1/v2/sale-order/shop/table/check'
        payload = '{"tableNo":"'+self.tableCode+'","tableName":"'+self.tableCode+'","shopCode":"'+self.shopCode+'"}'
        response = requests.request("POST", url, headers=self.headers, data=payload)
        self.orderNo = Tool.get_json_result(response, '$.data.orderNo')[0]
        self.logger.info('获取门店台位订单成功！\n请求参数:{0};\n响应内容：{1}'.format(payload, response.text))
        try:
            self.conn_redis.set('orderNo',self.orderNo)
            self.logger.info('订单号插入redis成功！插入订单号为：{};'.format(self.orderNo))
        except:
            self.logger.error('订单号插入redis失败')
        return response.text

    def cart_addFood(self):
        '''
        台位有订单加菜
        :return: 接口响应内容
        '''
        url = sys_cfg["api_sit_url"] + '/dianxin-mp/v1/v2/cart/addFood'
        payload = '{"businessType":1,"cartOrderType":1,"orderNo":"'+self.orderNo+'","shopCode":"'+self.shopCode+'","tableCode":"'+self.tableCode+'"}'
        response = requests.request("POST", url, headers=self.headers, data=payload)
        self.logger.info('点击「加菜」成功！\n请求参数:{0};\n响应内容：{1}'.format(payload, response.text))
        return response.text

    def cart_list(self):
        '''
        购物车列表
        :return:接口响应内容
        '''
        url = sys_cfg["api_sit_url"] + '/dianxin-mp/v1/v2/cart/list'
        payload = '{"businessType":1,"brandCode":"'+self.brandCode+'","cartOrderType":1,"shopCode":"'+self.shopCode+'","tableCode":"'+self.tableCode+'","tableName":"'+self.tableCode+'"}'
        response = requests.request("POST", url, headers=self.headers, data=payload)
        self.logger.info('获取购物车列表成功！\n请求参数:{0};\n响应内容：{1}'.format(payload, response.text))
        return response.text




if __name__ == '__main__':
    c = Order_Api_Test('17405339-f7a3-48d6-ba24-bc0a85fe21a4')
    c.cart_check_binding_table()
    c.save_people_number()
    c.cart_add()
    c.sale_order_submit()
    c.sale_order_detail()
    c.shop_table_check()
    c.cart_addFood()
    c.cart_add()
    c.sale_order_submit()
    c.sale_order_detail()