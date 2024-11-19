import json
from kafka import KafkaConsumer
import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.graph_objs as go
from collections import defaultdict

update_interval = 1000

app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.H1(children="Real-time Stock Prices"),
    dcc.Graph(id='live-graph', animate=True),
    dcc.Interval(id='graph-update', interval=update_interval) 
])

consumer = KafkaConsumer(
    'stocks',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='stock-group',
    value_deserializer=lambda v: json.loads(v.decode('utf-8')))

# Store historical data for each stock
price_history = defaultdict(lambda: {"time": [], "price": []})

@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])
def update_graph_scatter(n):
    # Poll for new messages with a timeout
    messages = consumer.poll(timeout_ms=update_interval, max_records=1000)
    for tp, msgs in messages.items():
        for msg in msgs:
            data = msg.value
            symbol = data['symbol']
            price_history[symbol]["time"].append(data['timestamp'])
            price_history[symbol]["price"].append(data['price'])

    fig = go.Figure()
    for symbol, data in price_history.items():
        fig.add_trace(go.Scatter(
            x=data["time"],
            y=data["price"],
            name=symbol,
            mode='markers'
        ))

    fig.update_layout(
        title="Stock Prices",
        xaxis_title="Time",
        yaxis_title="Price"
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)