import plotly.graph_objects as go
import matplotlib.pyplot as plt

def draw_candlestick(df):
  candlestick_data = go.Candlestick(
    x=df.index.tolist(),
    open=df['open'].tolist(),
    high=df['high'].tolist(),
    low=df['low'].tolist(),
    close=df['close'].tolist()
  )

  fig = go.Figure()
  fig.add_trace(candlestick_data)

  return fig
