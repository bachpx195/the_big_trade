from sqlalchemy import true
from .constants import OPEN_INDEX, CLOSE_INDEX
import pandas as pd

# ((col2 - col1) / col1) * 100

def percentage_change(df, col1_index, col2_index):
  return df.apply(lambda row: (row.iloc[col2_index]-row.iloc[col1_index])/row.iloc[col1_index]*100, axis=1)

def candlestick_type(df):
  return df.apply(lambda row: 'down' if row.iloc[OPEN_INDEX] > row.iloc[CLOSE_INDEX] else 'up', axis=1)

def candlestick_type_by_hour(df, hour):
  return df.apply(lambda row: calc_candlestick_type_by_hour(row, df, hour), axis=1)

def candlestick_first_15m(df_in_hour, df_in_minute):
  return df_in_hour.apply(lambda row: calc_candlestick_first_15m(row, df_in_minute), axis=1)

def type_continuous(df, sort_type='DESC'):
  return df.apply(lambda row: count_continuous(df, row, sort_type), axis=1)

def is_2h_in_open_price(df):
  """ Nếu giá của nến 2h và nến 7h trong ngày giao với nhau thì trả về true"""
  return df.apply(lambda row: calc_2h_in_open_price(df, row), axis=1)

def calc_2h_in_open_price(df, row):
  import datetime

  # import pdb; pdb.set_trace()
  current_time = row.day
  if row.hour < 7 and row.hour >= 0:
    try:
      previous_day = (datetime.datetime.strptime(current_time, "%Y-%m-%d") - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

      # lấy row đầu tiên sau khi query
      data_2h = df[(df['day'] == current_time) & (df['hour'] == 2)].iloc[0]
      data_7h = df[(df['day'] == previous_day) & (df['hour'] == 7)].iloc[0]

      if data_2h is None or data_7h is None:
        return False

      if (data_7h.high >= data_2h.low and data_2h.low >= data_7h.low) or (data_7h.high >= data_2h.high and data_2h.high >= data_7h.low):
        return False
      else:
        print("_______7h_______")
        print(data_7h)
        print("_______2h_______")
        print(data_2h)

        return True
    except:
      return ''
  else:
    return False

def count_continuous(df, row, sort_type='DESC'):
  count = 0
  while True:
    shift_number = -(count + 1) if sort_type == 'ASC' else count + 1
    if df.shift(shift_number).loc[row.name].type != row.type:
      break
    count = count + 1
  return count if count == 0 else count + 1

def until_now_type(df):
  return df.apply(lambda row: calc_until_now_type(row, df), axis=1)

def calc_candlestick_type_by_hour(row, df, hour):
  try:
    return df[(df['day'] == row.day) & (df['hour'] == hour)].iloc[-1]['type']
  except:
    return ''

def calc_candlestick_first_15m(row, df_in_minute):
  time = row.name + pd.Timedelta(minutes = 15)
  first_15m = df_in_minute[(df_in_minute.index == time)]

  if first_15m.empty:
    return ''
  else:
    return first_15m.type.iloc[0]


def calc_until_now_type(row, df):
  try:
    return 'down' if df[(df['day'] == row.day) & (df['hour'] == 7)].iloc[-1]['open'] < row.iloc[OPEN_INDEX] else 'up'
  except:
    return ''

def phi_coefficient(df, col1, col2):
  # https://en.wikipedia.org/wiki/Phi_coefficient

  from sklearn.metrics import matthews_corrcoef

  y_true = [x for x in df[col1].to_list() if x]
  y_pred = [x for x in df[col2].to_list() if x]

  return matthews_corrcoef(y_true, y_pred)

def diff_days(start_date, end_date, format):
  from datetime import datetime

  a = datetime.strptime(start_date, format)
  b = datetime.strptime(end_date, format)
  delta = b - a

  return delta.days

def unique_list(list):
  list2 = []
  for i in list:
    if not i in list2:
      list2.append(i)
  return list2

def max_high_and_low(df):
  """Lấy đỉnh và đáy của một zone"""

  return df.high.max(), df.low.min()
