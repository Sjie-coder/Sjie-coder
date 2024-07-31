'''
Author: Shao Jie
Date: 2024-07-26 14:15:11
LastEditors: Shao Jie
LastEditTime: 2024-07-30 14:57:10
'''


from flask import Flask, request
import json
# from waitress import serve
# import logging
# import sys
# import time

'''注册Flask服务'''
app = Flask(__name__)


'''模型预测服务'''
@app.route('/arrival_departure_throughput_efficiency', methods=['POST'])
def arrival_departure_throughput_efficiency():
    """
    机场进离场吞吐效率
    :param arrival_departure_throughput: 机场进离场吞吐量, int
    :param arrival_departure_capacity: 机场进离场容量, int
    :param arrival_departure_requirement: 机场进离场需求, int
    :return: 机场进离场吞吐效率, float
    """

    app.logger.info('收到请求') 

    # 提取数据
    data = request.json

    if "arrival_departure_throughput" and "arrival_departure_capacity" and "arrival_departure_requirement" in data:
        if (data["arrival_departure_throughput"] and data["arrival_departure_capacity"] and data["arrival_departure_requirement"])  != None:
            arrival_departure_throughput = data["arrival_departure_throughput"]
            arrival_departure_capacity = data["arrival_departure_capacity"]
            arrival_departure_requirement = data["arrival_departure_requirement"]
        else:
            return json.dumps({"alarm":"请注意输入的参数是否为空！"}, ensure_ascii=False)
    else:
       return json.dumps({"alarm":"请输入必要参数！"}, ensure_ascii=False)
    
    if arrival_departure_requirement < arrival_departure_capacity: 
        throughput_efficiency = round(arrival_departure_throughput/arrival_departure_requirement, 2)
    else: 
        throughput_efficiency = round(arrival_departure_throughput/arrival_departure_capacity, 2)

    return json.dumps({"机场进离场吞吐效率":throughput_efficiency}, ensure_ascii=False)

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, threaded=False)