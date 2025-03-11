import sqlite3
import time
import os
import pandas as pd
from schedule import every, repeat, run_pending
from data_generator import generate_sensor_data
from ai_model import train_model, predict_anomalies  # 导入训练和预测函数

def save_to_db(data):
    conn = sqlite3.connect('data/sensor_data.db')
    data.to_sql('sensor_data', conn, if_exists='append', index=False)
    conn.close()

def get_polling_interval():
    # 根据系统负载或业务需求动态调整轮询周期
    # 例如，根据 CPU 使用率或数据生成频率调整
    return 30  # 默认 30 秒

def initialize_db():
    # 检查数据库文件是否存在
    if not os.path.exists('data/sensor_data.db'):
        print("数据库文件不存在，创建数据库并生成初始数据...")
        os.makedirs('data', exist_ok=True)  # 创建 data 目录
        initial_data = generate_sensor_data(1000, 0.1)  # 生成 1000 条初始数据
        save_to_db(initial_data)
        print("初始数据已保存。")
    else:
        # 检查数据库中是否有数据
        conn = sqlite3.connect('data/sensor_data.db')
        try:
            data = pd.read_sql('SELECT * FROM sensor_data LIMIT 1', conn)
            if data.empty:
                print("数据库为空，生成初始数据...")
                initial_data = generate_sensor_data(1000, 0.1)  # 生成 1000 条初始数据
                save_to_db(initial_data)
                print("初始数据已保存。")
        finally:
            conn.close()

@repeat(every(get_polling_interval()).seconds)
def job():
    data = generate_sensor_data(5, 0.1)  # 每次生成 50 条数据，异常概率为 10%
    save_to_db(data)
    # print("数据已保存:", data.iloc[0])

    # 调用 AI 模型进行预测
    predict_anomalies()

@repeat(every(1).hours)  # 每隔 1 小时重新训练模型
def retrain_model():
    print("开始重新训练模型...")
    train_model()
    print("模型重新训练完成。")

if __name__ == "__main__":
    # 初始化数据库
    initialize_db()

    # 启动时检查模型是否存在，如果不存在则训练
    if not os.path.exists('ai_model.pkl'):
        print("模型未训练，开始训练模型...")
        train_model()

    while True:
        run_pending()
        time.sleep(get_polling_interval())  # 动态调整轮询周期