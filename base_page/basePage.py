# -*- coding+: utf-8 -*-
"""
@author:Kirito
@file:basePage.py
@time:2021/06/08
@describe：selenium关键词封装：用于封装各类行为操作，便于页面对象进行调用
"""
from selenium import webdriver
import os, time
from selenium.webdriver.support.wait import WebDriverWait
from Comm.logger import Logger

# 基础目录
_baseHome = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BesePage():

    def __init__(self,driver):
        self.logger = Logger().logger
        self.driver = driver
        # 添加隐式等待（10S）
        self.driver.implicitly_wait(10)

    def open_url(self, url):
        '''
        打开对应网站
        :param url: 需要访问的地址
        :return: none
        '''
        self.logger.info("正在打开网址：{}".format(url))
        self.driver.get(url)

    def quit_browser(self):
        '''
        关闭浏览器
        :return: none
        '''
        self.logger.info("正在退出浏览器～")
        self.driver.quit()

    def get_element(self, locator):
        '''
        查找对应元素
        :param locator: 定位器，元素定位（元祖类型：元素定位类型，元素定位方式）
        :return: 返回查找到的元素
        '''
        self.logger.info("查找元素：{}".format(locator))
        return self.driver.find_element(*locator)


    def click_element(self, locator):
        '''
        点击元素操作
        :param locator:定位器，元素定位（元祖类型：元素定位类型，元素定位方式）
        :return:none
        '''
        self.logger.info("点击元素：{}".format(locator))
        self.get_element(locator).click()

    def input_text(self, locator, txt):
        '''
        输入操作
        :param locator: 定位器，元素定位（元祖类型：元素定位类型，元素定位方式）
        :param txt:输入文本
        :return:none
        '''
        self.logger.info("{}:元素输入内容：{}".format(locator,txt))
        self.get_element(locator).send_keys(txt)

    def sleep(self, times=3):
        '''
        强制等待
        :param times: 默认3S
        :return: none
        '''
        self.logger.info("强制等待：{}秒，休息一会～".format(times))
        time.sleep(times)

    def get_element_txt(self, locator):
        '''
        获取元素文本内容
        :param locator: 定位器，元素定位（元祖类型：元素定位类型，元素定位方式）
        :return:元素文本内容
        '''
        self.logger.info("正在进行获取{}元素文本内容～".format(locator))
        return self.get_element(locator).text

    def element_clear(self, locator):
        '''
        清空元素内容
        :param locator: 定位器，元素定位（元祖类型：元素定位类型，元素定位方式）
        :return:none
        '''
        self.logger.info("正在对{}元素进行清空内容操作～".format(locator))
        self.get_element(locator).clear()

    def keyboard_keys(self,locator,keys):
        '''
        键盘按键操作
        :param locator: 定位器，元素定位（元祖类型：元素定位类型，元素定位方式）
        :param keys: 需要操作的按键名，大写
        :return: none
        :常用按键有：
                BACK_SPACE - 退格按钮
                TAB - Tab 按钮
                SHIFT - Shift 按钮
                ALT - Alt按钮
                SPACE - 空格按钮
                PAGE_UP - 向上翻页按钮
                PAGE_DOWN - 向下翻页按钮
                F12 - 打开控制台
                COMMAND - Win 按钮
        '''
        if keys == 'END':
            self.get_element(locator).send_keys(Keys.END)
            self.logger.info('正在对页面元素{locator}操作{keys}操作～'.format(locator,keys))
        elif keys == 'HOME':
            self.get_element(locator, doc).send_keys(Keys.HOME)
            self.logger.info('正在对页面元素{locator}操作{keys}操作～'.format(locator,keys))
        elif keys == 'BACK_SPACE':
            self.get_element(locator, doc).send_keys(Keys.BACK_SPACE)
            self.logger.info('正在对页面元素{locator}操作{keys}操作～'.format(locator,keys))
        elif keys == 'TAB':
            self.get_element(locator, doc).send_keys(Keys.TAB)
            self.logger.info('正在对页面元素{locator}操作{keys}操作～'.format(locator,keys))
        elif keys == 'SHIFT':
            self.get_element(locator, doc).send_keys(Keys.SHIFT)
            self.logger.info('正在对页面元素{locator}操作{keys}操作～'.format(locator,keys))
        elif keys == 'ALT':
            self.get_element(locator, doc).send_keys(Keys.ALT)
            self.logger.info('正在对页面元素{locator}操作{keys}操作～'.format(locator,keys))
        elif keys == 'SPACE':
            self.get_element(locator, doc).send_keys(Keys.SPACE)
            self.logger.info('正在对页面元素{locator}操作{keys}操作～'.format(locator,keys))
        elif keys == 'PAGE_UP':
            self.get_element(locator, doc).send_keys(Keys.PAGE_UP)
            self.logger.info('正在对页面元素{locator}操作{keys}操作～'.format(locator,keys))
        elif keys == 'PAGE_DOWN':
            self.get_element(locator, doc).send_keys(Keys.PAGE_DOWN)
            self.logger.info('正在对页面元素{locator}操作{keys}操作～'.format(locator,keys))
        elif keys == 'F12':
            self.get_element(locator, doc).send_keys(Keys.F12)
            self.logger.info('正在对页面元素{locator}操作{keys}操作～'.format(locator,keys))
        elif keys == 'COMMAND':
            self.get_element(locator, doc).send_keys(Keys.COMMAND)
            self.logger.info('正在对页面元素{locator}操作{keys}操作～'.format(locator,keys))
