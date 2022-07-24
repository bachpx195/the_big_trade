import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
from apps.helpers.datetime_helper import next_day


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

  fig.update_layout(xaxis_rangeslider_visible=False)

  return fig

# format date = 2022-07-22
def draw_candlestick_by_day(df, date):
  df = df[(df['day'] == date) | (df['day'] == next_day(date))]

  candlestick_data = go.Candlestick(
    x=df.index.tolist(),
    open=df['open'].tolist(),
    high=df['high'].tolist(),
    low=df['low'].tolist(),
    close=df['close'].tolist()
  )

  fig = go.Figure()
  fig.add_trace(candlestick_data)

  fig.update_layout(xaxis_rangeslider_visible=False)

  return fig

def draw_candlestick_use_zones(df, zones):
  df = df.iloc[::-1]

  tickvals =[k*0.5 for k in range(len(df))]
  ticktext=list((date.to_pydatetime().strftime("%Y-%m-%d %Hh") for date in df.index))

  fig = go.Figure(data=[go.Candlestick(x=tickvals, #df['data_minu'],
                  open=df['open'], high=df['high'],
                  low=df['low'], close=df['close'])])

  fig.update_layout(xaxis_rangeslider_visible=False, xaxis_tickvals=tickvals, xaxis_ticktext=ticktext)

  for zone in zones:
    fig.add_shape(dict(type='rect',
                      xref='x', yref='y',
                      layer='below',
                      x0 = tickvals[zone.end]  - 0.2, y0 = zone.low,
                      x1 = tickvals[zone.start] + 0.2, y1 = zone.high,
                      fillcolor='orange', #'RoyalBlue',
                      opacity=0.35))

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

def draw_pie_chart(df):
  labels = df.index.values
  sizes = df.values

  plt.figure()
  fig1, ax1 = plt.subplots(figsize=(12, 7))
  ax1.pie(sizes, labels=labels, autopct='%1.1f%%')
  ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

  plt.legend()
  return plt

def draw_bar_horizontal_chart(df):
  plt.figure()
  highest_in_day_group = df.groupby(
      'day').mean().groupby('highest_in_day').count()

  list_hours = [int(hour) for hour in highest_in_day_group.index.values.tolist()]
  list_highest_in_day = highest_in_day_group['hour'].tolist()

  plt.rcParams['figure.figsize'] = [10, 10]

  fig, ax = plt.subplots()
  ax.barh(list_hours, list_highest_in_day, align='center')

  ax.set_yticks(list_hours)
  ax.set_yticklabels(list_hours)
  ax.set_xticks([])

  ax2 = ax.twinx()
  ax2.set_ylim(ax.get_ylim())
  ax2.set_yticks(list_hours)
  ax2.set_yticklabels(list_highest_in_day)

  return plt
