import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
from apps.helpers.datetime_helper import next_day
from apps.helpers.utils import max_high_and_low, refactor_list_of_float, find_highest_and_lower_hour


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

  fig.update_layout(xaxis_rangeslider_visible=False, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))

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

  fig.update_layout(xaxis_rangeslider_visible=False, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))

  for zone in zones:
    fig.add_shape(dict(type='rect',
                      xref='x', yref='y',
                      layer='below',
                      x0 = tickvals[zone.end]  - 0.2, y0 = zone.low,
                      x1 = tickvals[zone.start] + 0.2, y1 = zone.high,
                      fillcolor='orange', #'RoyalBlue',
                      opacity=0.35))

  return fig

def draw_candlestick_diff(df):
  from apps.models.zone import Zone
  df = df.iloc[::-1]

  if len(df) > 31:
    end = 31
  else:
    end = len(df) - 1

  date_df = df[7:end]
  # import pdb; pdb.set_trace()
  high, low = max_high_and_low(date_df)

  zone = Zone(7, end, high, low)

  tickvals =[k*0.5 for k in range(len(df))]
  ticktext=list((date.to_pydatetime().strftime("%Y-%m-%d %Hh") for date in df.index))

  fig = go.Figure(data=[go.Candlestick(x=tickvals, #df['data_minu'],
                  open=df['open'], high=df['high'],
                  low=df['low'], close=df['close'])])

  fig.update_layout(xaxis_rangeslider_visible=False, xaxis_tickvals=tickvals, xaxis_ticktext=ticktext, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))


  fig.add_shape(dict(type='rect',
                    xref='x', yref='y',
                    layer='below',
                    x0 = tickvals[zone.end]  + 0.2, y0 = zone.low,
                    x1 = tickvals[zone.start] - 0.2, y1 = zone.high,
                    fillcolor='orange', #'RoyalBlue',
                    opacity=0.35))

  return fig

def draw_candlestick_morning_session(df):
  try:
    from apps.models.zone import Zone

    # Đảo ngược dataframe
    df = df.iloc[::-1]

    if len(df) > 40:
      end = 40
    else:
      end = len(df) - 1

    date_df = df[31:end]
    high, low = max_high_and_low(date_df)

    zone = Zone(31, end, high, low)

    tickvals =[k*0.5 for k in range(len(df))]
    ticktext=list((date.to_pydatetime().strftime("%Y-%m-%d %Hh") for date in df.index))

    fig = go.Figure(data=[go.Candlestick(x=tickvals, #df['data_minu'],
                    open=df['open'], high=df['high'],
                    low=df['low'], close=df['close'])])

    fig.update_layout(xaxis_rangeslider_visible=False, xaxis_tickvals=tickvals, xaxis_ticktext=ticktext, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))

    fig.add_shape(dict(type='rect',
                      xref='x', yref='y',
                      layer='below',
                      x0 = tickvals[zone.end]  + 0.2, y0 = zone.low,
                      x1 = tickvals[zone.start] - 0.2, y1 = zone.high,
                      fillcolor='orange', #'RoyalBlue',
                      opacity=0.35))

    return fig
  except:
    fig = go.Figure()
    return fig
  
def draw_candlestick_with_highest_and_lowest_zone(df):
  # try:
  from apps.models.zone import Zone

  # Đảo ngược dataframe
  df = df.iloc[::-1]

  highest_hour, lowest_hour, highest, lowest = find_highest_and_lower_hour(df)

  highest_number = highest_hour - 7 if highest_hour >= 7 else highest_hour + 17
  lowest_number = lowest_hour - 7 if lowest_hour >= 7 else lowest_hour + 17
  zone_highest = Zone(highest_number, highest_number, highest, lowest)
  zone_lowest = Zone(lowest_number, lowest_number, highest, lowest)


  tickvals =[k*0.5 for k in range(len(df))]
  ticktext=list((date.to_pydatetime().strftime("%Y-%m-%d %Hh") for date in df.index))

  fig = go.Figure(data=[go.Candlestick(x=tickvals, #df['data_minu'],
                  open=df['open'], high=df['high'],
                  low=df['low'], close=df['close'])])

  fig.update_layout(xaxis_rangeslider_visible=False, xaxis_tickvals=tickvals, xaxis_ticktext=ticktext, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))

  fig.add_shape(dict(type='rect',
                    xref='x', yref='y',
                    layer='below',
                    x0 = tickvals[zone_highest.end]  + 0.2, y0 = zone_highest.low,
                    x1 = tickvals[zone_highest.start] - 0.2, y1 = zone_highest.high,
                    fillcolor='orange', #'RoyalBlue',
                    opacity=0.35))

  fig.add_shape(dict(type='rect',
                    xref='x', yref='y',
                    layer='below',
                    x0 = tickvals[zone_lowest.end]  + 0.2, y0 = zone_lowest.low,
                    x1 = tickvals[zone_lowest.start] - 0.2, y1 = zone_lowest.high,
                    fillcolor='pink', #'RoyalBlue',
                    opacity=0.35))

  return fig
  # except:
  #   fig = go.Figure()
  #   return fig

def draw_candlestick_day_session(df):
  try:
    df = df.iloc[::-1]
    tickvals =[k*0.5 for k in range(len(df))]
    ticktext=list((date.to_pydatetime().strftime("%Y-%m-%d %Hh") for date in df.index))

    fig = go.Figure(data=[go.Candlestick(x=tickvals, #df['data_minu'],
                    open=df['open'], high=df['high'],
                    low=df['low'], close=df['close'])])

    fig.update_layout(xaxis_rangeslider_visible=False, xaxis_tickvals=tickvals, xaxis_ticktext=ticktext, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))

    return fig
  except:
    fig = go.Figure()
    return fig

def draw_candlestick_2h(df, date):
  from apps.models.zone import Zone
  df = df.iloc[::-1]

  hour_2h = df[(df['day'] == date) & (df['hour'] == 2)]

  zone = Zone(26, 30, hour_2h.high.values[0], hour_2h.low.values[0])

  tickvals =[k*0.5 for k in range(len(df))]
  ticktext=list((date.to_pydatetime().strftime("%Y-%m-%d %Hh") for date in df.index))

  fig = go.Figure(data=[go.Candlestick(x=tickvals, #df['data_minu'],
                  open=df['open'], high=df['high'],
                  low=df['low'], close=df['close'])])

  fig.update_layout(xaxis_rangeslider_visible=False, xaxis_tickvals=tickvals, xaxis_ticktext=ticktext, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))

  fig.add_shape(dict(type='rect',
                    xref='x', yref='y',
                    layer='below',
                    x0 = tickvals[zone.end]  + 0.2, y0 = zone.low,
                    x1 = tickvals[zone.start] - 0.2, y1 = zone.high,
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

def draw_histogram(list, bin=10, round_number=2):
  fig, ax = plt.subplots()
  # import pdb; pdb.set_trace();
  ax.hist(refactor_list_of_float(list, round_number), bins=bin)

  return fig

def draw_simple_barchart(label_list, value_list):
  fig = plt.figure(figsize = (10, 5))

  # creating the bar plot
  plt.bar(label_list, value_list, color ='maroon',
          width = 0.4)

  plt.xlabel("Courses offered")
  plt.ylabel("No. of students enrolled")
  plt.title("Students enrolled in different courses")


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


def draw_inside_and_outside_pie_chart(sizes,labels):
  plt.figure()
  fig1, ax1 = plt.subplots(figsize=(12, 7))
  ax1.pie(sizes, labels=labels, autopct='%1.1f%%')
  ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

  plt.legend()

  return plt

def draw_inside_and_outside_week_bar_chart(n_groups, max_in_week, min_in_week):
  fig, ax = plt.subplots()
  index = np.arange(n_groups)
  bar_width = 0.35
  opacity = 0.8

  rects1 = plt.bar(index, max_in_week, bar_width,
                  alpha=opacity, color='b', label='Giá cao nhất')

  rects2 = plt.bar(index + bar_width, min_in_week, bar_width,
                  alpha=opacity, color='g', label='Giá thấp nhất')

  plt.xlabel('Ngày')
  plt.ylabel('Số lần')
  plt.title(
      f"Hiệu ứng ngày trong tuần và hành vi của thị trường")
  plt.xticks(index + bar_width, ('Thứ 2', 'Thứ 3',
                                'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ nhật'))
  plt.legend()
  plt.tight_layout()

  return plt
