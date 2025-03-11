import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import sqlite3

# 创建Dash应用
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='live-graph'),
    dcc.Interval(id='graph-update', interval=1000, n_intervals=0)
])

@app.callback(Output('live-graph', 'figure'),
              Input('graph-update', 'n_intervals'))
def update_graph(n):
    conn = sqlite3.connect('data/sensor_data.db')
    data = pd.read_sql('SELECT * FROM sensor_data_with_anomalies ORDER BY timestamp DESC LIMIT 100', conn)
    conn.close()

    # 标记异常数据
    data['color'] = data['anomaly'].apply(lambda x: 'red' if x == -1 else 'blue')

    fig = px.scatter(data, x='timestamp', y='temperature', color='color',
                     title='传感器数据实时监控（红色为异常数据）')
    return fig

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8050)