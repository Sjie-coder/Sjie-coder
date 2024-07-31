from flask import Flask, request
import json
# from waitress import serve
# import logging
# import sys
# import time

'''注册Flask服务'''
app = Flask(__name__)


'''模型预测服务'''
@app.route('/checkin_capacity', methods=['POST'])
def checkin_capacity():   # num_checkin_counters, num_checkin_queue, mu=2, w=8
    """
    值机业务区域理论值机容量计算函数
    :param num_checkin_counters: 区域当前开放值机柜台数量, int
    :param num_checkin_queue: 区域排队人数, int
    :param mu: 单个值机柜台每分钟服务旅客数的经验值, float
    :param w: 95%旅客的最大等待时间, int
    :return: 区域每小时理论容量 int, 告警信息 str
    """

    app.logger.info('收到请求') 

    # 提取数据
    data = request.json

    if "num_checkin_counters" and "num_checkin_queue" in data:
        if (data["num_checkin_counters"] and data["num_checkin_queue"])  != None:
            num_checkin_counters = data["num_checkin_counters"]
            num_checkin_queue = data["num_checkin_queue"]
        else:
            return json.dumps({"alarm":"请注意输入的参数是否为空！"}, ensure_ascii=False)
    else:
       return json.dumps({"alarm":"请输入必要参数！"}, ensure_ascii=False)
    
    mu=data["mu"] if "mu" in data else 2
    w=data["w"] if "w" in data else 8

    capacity = num_checkin_counters * mu * w
    alarm = '值机理论容量充足' if capacity >= num_checkin_queue * 0.95 else '值机资源紧缺'
    return json.dumps({"区域每小时理论容量":int(capacity * 60 / w),"alarm":alarm}, ensure_ascii=False)

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, threaded=False)