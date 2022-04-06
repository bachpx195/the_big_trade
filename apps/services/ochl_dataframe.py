from apps.helpers.constants import HIGH_INDEX, LOW_INDEX, OPEN_INDEX, CLOSE_INDEX
from apps.helpers.utils import percentage_change, candlestick_type, type_continuous, until_now_type, candlestick_type_by_hour


def add_return_column(df):
  df['hour_return'] = percentage_change(df, OPEN_INDEX, CLOSE_INDEX)
  return df

def add_day_column(df):
  df['day'] = df[['open']].apply(lambda x: x.name.strftime("%Y-%m-%d"), axis=1)
  return df

def add_hour_column(df):
  df['hour'] = df[['open']].apply(lambda x: x.name.hour, axis=1)
  return df

def add_agv_oc(df):
  df['average_oc'] = df.apply(lambda row: (row.iloc[OPEN_INDEX]+row.iloc[CLOSE_INDEX])/2, axis=1)
  return df