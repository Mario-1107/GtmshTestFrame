# -*- coding+: utf-8 -*-
"""
@author:Kirito
@file:logger.py
@time:2021/06/08
@describe：日志封装
"""
import logging
import os, time
from logging.handlers import TimedRotatingFileHandler
from Config.yamlReader import log_cfg


class Logger():
    # 项目基础目录
    _beseHome = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    def __init__(self):

        # 日志等级：log_level取过来是个字符串，没法直接用，通过eval执行后，就变成了logging定义的对象
        _log_level = eval(log_cfg['log_level'])
        _log_path = log_cfg['log_path']
        _log_format = log_cfg['log_format']
        # 定义日志文件存放路径
        _log_file = os.path.join(self._beseHome, _log_path, 'log.log')
        # 创建日志器
        self.logger = logging.getLogger('Mario')
        # 设置日志等级
        self.logger.setLevel(level=_log_level)
        # 设置日志格式
        formatter = logging.Formatter(_log_format)
        # 使用TimedRotatingFileHandler实现滚动日志
        '''
            handler用于向日志文件打印日志;
            filename:日志文件
            when:切割条件(按周(W)、天(D)、时(H)、分(M)、秒(S)切割)
            interval:间隔(就是几个when切割一次。when是W，interval是3的话就代表3周切割一次)
            backupCount:日志备份数量(就是保留几个日志文件，起过这个数量，就把最早的删除掉，从而滚动删除)
        '''
        handler = TimedRotatingFileHandler(filename=_log_file, when='D', interval=1, backupCount=7)
        #向日志文件打印日志
        handler.setLevel(_log_level)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        #向控制台打印日志
        console = logging.StreamHandler()
        console.setLevel(_log_level)
        console.setFormatter(formatter)
        self.logger.addHandler(console)

if __name__ == '__main__':
    logger = Logger().logger
    logger.debug("这是 log 模块测试内容1")
    logger.info("这是 log 模块测试内容2")
    logger.warning("这是 log 模块测试内容3")
    logger.error("这是 log 模块测试内容4")
    logger.critical("这是 log 模块测试内容5")
