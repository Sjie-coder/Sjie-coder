from flask import Flask, request
import json
# from waitress import serve
# import logging
# import sys
# import time

'''注册Flask服务'''
app = Flask(__name__)


'''模型预测服务'''
@app.route('/security_check_capacity', methods=['POST'])
def security_check_capacity():         # num_security_check_channels, num_security_check_queue, mu=2, w=8
    """
    安检业务理论值机容量计算函数, 普通安检和VIP安检应分别传参调用本函数
    :param num_security_check_channels: 区域当前开放安检通道数量, int
    :param num_security_check_queue: 区域排队人数, int
    :param mu: 单个安检通道每分钟服务旅客数的经验值, float
    :param w: 95%旅客的最大等待时间, int
    :return: 区域每小时理论容量 int, 告警信息 str
    """

    app.logger.info('收到请求') 
    # 提取数据
    data = request.json
    if "num_security_check_channels" and "num_security_check_queue" in data:
        if (data["num_security_check_channels"] and data["num_security_check_queue"])  != None:
            num_security_check_channels = data["num_security_check_channels"]
            num_security_check_queue = data["num_security_check_queue"]
        else:
            return json.dumps({"alarm":"请注意输入的参数是否为空！"}, ensure_ascii=False)
    else:
       return json.dumps({"alarm":"请输入必要参数！"}, ensure_ascii=False)
    
    mu=data["mu"] if "mu" in data else 2
    w=data["w"] if "w" in data else 8

    capacity = num_security_check_channels * mu * w
    alarm = '安检理论容量充足' if capacity >= num_security_check_queue * 0.95 else '安检资源紧缺'
    return json.dumps({"区域每小时理论容量":int(capacity * 60 / w), "alarm":alarm}, ensure_ascii=False)

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000, threaded=False)