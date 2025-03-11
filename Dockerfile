FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
#RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 启动数据生成,AI 预测和可视化
CMD bash -c "python src/data_collector.py & python src/dashboard.py"
