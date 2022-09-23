from apps.helpers.constants import HIGH_INDEX, LOW_INDEX, OPEN_INDEX, CLOSE_INDEX
from apps.helpers.utils import percentage_change, candlestick_type, type_continuous, until_now_type, candlestick_type_by_hour, is_2h_in_open_price


def add_return_column(df):
  df['hour_return'] = percentage_change(df, OPEN_INDEX, CLOSE_INDEX)
  return df

def add_volatility_column(df):
  df['volatility_return'] = percentage_change(df, HIGH_INDEX, LOW_INDEX)
  return df

def add_day_return_column(df):
  df['day_return'] = percentage_change(df, OPEN_INDEX, CLOSE_INDEX)
  return df

def add_day_column(df):
  df['day'] = df[['open']].apply(lambda x: x.name.strftime("%Y-%m-%d"), axis=1)
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
