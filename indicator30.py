from flask import Flask, request
import json
# from waitress import serve
# import logging
# import sys
# import time

'''注册Flask服务'''
app = Flask(__name__)


'''模型预测服务'''
@app.route('/checkin_flight_service_capacity', methods=['POST'])
def checkin_flight_service_capacity():  # total_checkin_capacity, num_predicted_departures, s=100, r=0.6
    """
    值机业务每小时能支持的最大离港航班数量计算函数
    :param total_checkin_capacity: 航站楼当前小时所有值机区域总理论值机容量, int
    :param num_predicted_departures: 当前小时预计离港航班数量, int
    :param s: 航班平均座位数经验值, int
    :param r: 航班平均上座率经验值, float
    :return: 值机业务当前小时能支持的最大离港航班数量 int, 告警信息 str,
    """

    app.logger.info('收到请求') 

    # 提取数据
    data = request.json
    if "total_checkin_capacity" and "num_predicted_departures" in data:
        if (data["total_checkin_capacity"] and data["num_predicted_departures"])  != None:
            total_checkin_capacity = data["total_checkin_capacity"]
            num_predicted_departures = data["num_predicted_departures"]
        else:
            return json.dumps({"alarm":"请注意输入的参数是否为空！"}, ensure_ascii=False)
    else:
       return json.dumps({"alarm":"请输入必要参数！"}, ensure_ascii=False)
    
    s=data["s"] if "s" in data else 100
    r=data["r"] if "r" in data else 0.6

    N = int(total_checkin_capacity / s / r)
    alarm = '值机理论容量充足' if N >= num_predicted_departures else '值机资源紧缺'
    return json.dumps({"值机业务当前小时能支持的最大离港航班数量":N, "alarm":alarm}, ensure_ascii=False)

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, threaded=False)