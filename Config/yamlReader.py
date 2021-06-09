# -*- coding+: utf-8 -*-
"""
@author:Kirito
@file:yamlReader.py
@time:2021/06/08
@describe：yaml文件读写
"""
import os, yaml


class YamlReader():

    def __init__(self):
        '''
        构造函数
        '''
        # 使用相对目录确定配置文件位置
        _conf_dir = os.path.dirname(__file__)
        _conf_file = os.path.join(_conf_dir, 'config.yaml')
        # 读取yaml文件
        with open(_conf_file, 'rb') as yaml_file:
            yaml_file_reader = yaml_file.read()
            self._yaml_result_datas = yaml.load(yaml_file_reader, yaml.FullLoader)

    def reader_yaml_datas(self, config_item: str):
        '''
        获取yaml文件配置信息
        :param config_item: 需要获取的第一个键
        :return:返回对应键下面的所有配置信息
        '''
        _item_config_data = self._yaml_result_datas[config_item]
        return _item_config_data


# 将各配置读取出来，放在变量里面，后续其他文件直接引用这些变量
config = YamlReader()
sys_cfg = config.reader_yaml_datas('sys')
log_cfg = config.reader_yaml_datas('log')
tapd_cfg = config.reader_yaml_datas('tapd')
smtp_cfg = config.reader_yaml_datas('smtp')
email_cfg = config.reader_yaml_datas('email')
