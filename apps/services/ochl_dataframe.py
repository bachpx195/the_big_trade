from apps.helpers.constants import HIGH_INDEX, LOW_INDEX, OPEN_INDEX, CLOSE_INDEX
from apps.helpers.utils import percentage_change, candlestick_type, type_continuous, until_now_type, candlestick_type_by_hour, is_2h_in_open_price
from apps.helpers.datetime_helper import previous_day

def add_return_column(df):
  df['hour_return'] = percentage_change(df, OPEN_INDEX, CLOSE_INDEX)
  return df

def add_volatility_column(df):
  df['volatility_return'] = percentage_change(df, LOW_INDEX, HIGH_INDEX)
  return df

def add_day_name_column(df):
  df['day_name'] = df[['open']].apply(lambda x: x.name.strftime("%A"), axis=1)
  return df

def add_day_return_column(df):
  df['day_return'] = percentage_change(df, OPEN_INDEX, CLOSE_INDEX)
  return df

def add_month_return_column(df):
  df['month_return'] = percentage_change(df, OPEN_INDEX, CLOSE_INDEX)
  return df

def add_month_hl_return_column(df):
  df['month_return_hl'] = percentage_change(df, LOW_INDEX, HIGH_INDEX)
  return df

def add_month_ol_return_column(df):
  df['month_return_ol'] = percentage_change(df, LOW_INDEX, OPEN_INDEX)
  return df

def add_month_ho_return_column(df):
  df['month_return_ho'] = percentage_change(df, HIGH_INDEX, OPEN_INDEX)
  return df

def add_day_volatility_column(df):
  df['day_volatility_return'] = percentage_change(df, LOW_INDEX, HIGH_INDEX)
  return df

def add_day_column(df):
  df['day'] = df[['open']].apply(lambda x: x.name.strftime("%Y-%m-%d"), axis=1)
  return df

# de doi chieu voi binance chart
def add_day_with_binance_column(df):
  df['day_with_binance'] = df[['open']].apply(lambda x: __day_with_binance(x.name), axis=1)
  return df

def add_month_column(df):
  df['month'] = df[['open']].apply(lambda x: x.name.strftime("%m"), axis=1)
  return df

def add_year_column(df):
  df['year'] = df[['open']].apply(lambda x: x.name.strftime("%Y"), axis=1)
  return df

def add_hour_column(df):
  df['hour'] = df[['open']].apply(lambda x: x.name.hour, axis=1)
  return df

def add_average_oc_column(df):
  df['average_oc'] = df.apply(lambda row: (row.iloc[OPEN_INDEX]+row.iloc[CLOSE_INDEX])/2, axis=1)
  return df

def add_rolling_average_oc_column(df):
  df['rolling_average_oc'] = df['average_oc'].rolling(2).mean()
  return df

def add_type_column(df):
  df['type'] = candlestick_type(df)
  return df

def add_type_continue_column(df, column_name=None):
  name = column_name if column_name else 'type_continuous'
  df[name] = type_continuous(df)
  return df

def add_2h_sideway_type(df):
  df['2h_type'] = is_2h_in_open_price(df)
  return df

def highest_in_day(df, x):
  max = df[df.day == x.day].hour_return.max()
  return df[(df.day == x.day) & (df.hour_return == max)].hour.iat[0]

def add_highest_in_day_column(df):
  df['highest_in_day'] = df[['day']].apply(lambda x: highest_in_day(df, x), axis=1)
  return df

def add_break_zone_return_column(df):
  """Trả về phần trăm vượt quá đinh hoặc đáy so với zone"""

def add_inside_bar_type_column(df):
  """0: trong biên độ/ 1: phá vỡ cả đỉnh và đáy/ 2 phá vỡ đáy/ 3 phá vỡ đỉnh"""
  data = [0]
  total = df.iloc[:,0].count()

  for index in range(0, total):
    if index < 1:
      continue

    # trong biên độ
    inside_bar_type = 0
    current_row = df.iloc[index]
    previous_row = df.iloc[index - 1]

    if current_row['low'] < previous_row['low'] and current_row['high'] > previous_row['high']:
      # Ngoài biên độ phá vỡ đỉnh và dáy
      inside_bar_type = 1
    elif current_row['low'] < previous_row['low']:
      # Ngoài biên độ phá vỡ dáy
      inside_bar_type = 2
    elif current_row['high'] > previous_row['high']:
      # Ngoài biên độ phá vỡ đỉnh
      inside_bar_type = 3

    data.append(inside_bar_type)

  df['inside_bar_type'] = data
  return df

def add_end_week_column(df):
  import datetime

  df['end_week'] = df[['high']].apply(
    lambda x: x.name.date() + datetime.timedelta(days=6), axis=1)

  return df

def min_low_in_week(row, df):
  df_week = __find_week_df(df, row)
  return df_week[df_week.low == df_week.low.min()].day_name[0]

def max_high_in_week(row, df):
  df_week = __find_week_df(df, row)
  return df_week[df_week.high == df_week.high.max()].day_name[0]

def min_vol_in_week(row, df):
  df_week = __find_week_df(df, row)
  return df_week[df_week.volumn == df_week.volumn.min()].day_name[0]

def max_vol_in_week(row, df):
  df_week = __find_week_df(df, row)
  return df_week[df_week.volumn == df_week.volumn.max()].day_name[0]

def add_min_low_in_week_column(df, day_df):
  df['min_low_in_week'] = df[[
    'end_week']].apply(lambda x: min_low_in_week(x,day_df), axis=1)
  return df

def add_max_high_in_week_column(df, day_df):
  df['max_high_in_week'] = df[[
    'end_week']].apply(lambda x: max_high_in_week(x,day_df), axis=1)
  return df

def add_min_vol_in_week_column(df, day_df):
  df['min_vol_in_week'] = df[[
    'end_week']].apply(lambda x: min_vol_in_week(x,day_df), axis=1)
  return df

def add_max_vol_in_week_column(df, day_df):
  df['max_vol_in_week'] = df[[
    'end_week']].apply(lambda x: max_vol_in_week(x,day_df), axis=1)
  return df

# Private function
def __find_week_df(df, row):
  return df[(df['day'] >= row.name.strftime("%Y-%m-%d")) & (df['day'] <= row['end_week'].strftime("%Y-%m-%d"))]

def __day_with_binance(time):
  if time.hour in [0,1,2,3,4,5,6]:
    return previous_day(time.strftime("%Y-%m-%d"))
  else:
    return time.strftime("%Y-%m-%d")