# -*- coding+: utf-8 -*-
"""
@author:Kirito
@file:test.py
@time:2021/06/08
@describe：
"""
import json
import flask

server = flask.Flask(__name__)
test1 = '1'


@server.route('/index', methods=['get'])
def index():
    res = {'msg': test1, 'msg_code': '0000'}
    return json.dumps(res, ensure_ascii=False)



if __name__ == '__main__':
    server.run(port=8999, debug=True, host='0.0.0.0')
