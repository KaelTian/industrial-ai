import pandas as pd
import numpy as np
import argparse
from datetime import datetime

def generate_sensor_data(num_samples, anomaly_prob=0.1):
    timestamps = pd.date_range(start=datetime.now(), periods=num_samples, freq="s")
    temperature = np.random.uniform(0, 100, num_samples)
    pressure = np.random.uniform(0, 10, num_samples)
    flow = np.random.uniform(0, 1000, num_samples)
    vibration = np.random.uniform(0, 10, num_samples)
    current = np.random.uniform(0, 20, num_samples)

    # 模拟异常数据
    anomaly_mask = np.random.rand(num_samples) < anomaly_prob
    if np.any(anomaly_mask):  # 确保至少有一条异常数据
        # 测试数据上只将温度和压力属性设置为异常值
        temperature[anomaly_mask] = np.random.uniform(100, 120, np.sum(anomaly_mask))  # 温度异常
        pressure[anomaly_mask] = np.random.uniform(10, 15, np.sum(anomaly_mask))       # 压力异常

    data = pd.DataFrame({
        "timestamp": timestamps,
        "temperature": temperature,
        "pressure": pressure,
        "flow": flow,
        "vibration": vibration,
        "current": current,
        "is_anomaly": anomaly_mask.astype(int)  # 标记异常数据
    })
    return data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="生成模拟传感器数据")
    parser.add_argument("--num_samples", type=int, default=100, help="生成的数据条数")
    parser.add_argument("--anomaly_prob", type=float, default=0.1, help="异常数据的概率")
    args = parser.parse_args()

    sensor_data = generate_sensor_data(args.num_samples, args.anomaly_prob)
    print(sensor_data.head())