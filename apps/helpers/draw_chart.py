import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np


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

def draw_time_distribution(df):
  bar_width = 0.35
  opacity = 0.8

  index = np.arange(24)
  bar_width = 0.35
  opacity = 0.8

  x = ()
  y = ()


  for i in np.arange(24):
      data_prices_x = df[df['hour'] == i]

      number_up = len(data_prices_x[data_prices_x['type'] == 'up'])
      number_down = len(data_prices_x[data_prices_x['type'] == 'down'])

      x = x + (number_up,)
      y = y + (number_down,)


  plt.figure(figsize=[20,10])
  plt.rcParams['figure.figsize'] = [10, 10]

  rects1 = plt.bar(index, x, bar_width,
                  alpha=opacity, color='b', label='up')

  rects2 = plt.bar(index + bar_width, y, bar_width,
                  alpha=opacity, color='r', label='down')
  plt.xlabel('Giờ')
  plt.ylabel('Hiệu ứng')
  plt.title(
      f"Hiệu ứng thời gian trong ngày")
  plt.xticks(index + bar_width, tuple(np.arange(24)))
  plt.legend()
  plt.tight_layout()

  return plt
