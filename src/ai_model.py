import pandas as pd
import sqlite3
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report
import joblib
import time

def train_model():
    # 加载历史数据
    conn = sqlite3.connect('data/sensor_data.db')
    data = pd.read_sql('SELECT * FROM sensor_data', conn)
    conn.close()

    # 选择特征
    features = ['temperature', 'pressure']  # 只使用温度和压力进行训练
    X = data[features]

    # 训练异常检测模型
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(X)

    # 保存模型
    joblib.dump(model, 'ai_model.pkl')
    print("模型已保存为 ai_model.pkl")

def predict_anomalies():
    # 加载模型
    model = joblib.load('ai_model.pkl')

    # 加载最新数据
    conn = sqlite3.connect('data/sensor_data.db')
    data = pd.read_sql('SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 100', conn)
    conn.close()

    # 选择特征
    features = ['temperature', 'pressure']  # 只使用温度和压力进行预测
    X = data[features]

    # 预测异常
    data['anomaly'] = model.predict(X)
    anomalies = data[data['anomaly'] == -1]  # 异常数据的标签为-1
    # print("检测到的异常数据：")
    # print(anomalies)

    # 评估模型
    if 'is_anomaly' in data.columns:
        y_true = data['is_anomaly'].replace({0: 1, 1: -1})  # 将 is_anomaly 转换为模型标签
        y_pred = data['anomaly']
        print("模型评估报告：")
        print(classification_report(y_true, y_pred, target_names=['正常', '异常']))

    # 将预测结果存储到数据库
    conn = sqlite3.connect('data/sensor_data.db')
    data.to_sql('sensor_data_with_anomalies', conn, if_exists='replace', index=False)
    conn.close()

if __name__ == "__main__":
    train_model()  # 训练模型
    predict_anomalies()  # 预测异常