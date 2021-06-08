# -*- coding+: utf-8 -*-
"""
@author:Kirito
@file:test.py
@time:2021/06/08
@describe：
"""
from Comm.logger import Logger

logger = Logger().logger

logger.debug("这是 vlog 模块测试内容1")
logger.info("这是 vlog 模块测试内容2")
logger.warning("这是 vlog 模块测试内容3")
logger.error("这是 vlog 模块测试内容4")
logger.critical("这是 vlog 模块测试内容5")
