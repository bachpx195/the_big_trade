from myenv.models.candlestick import Candlestick
from myenv.models.merchandise_rate import MerchandiseRate
from apps.services.ochl_dataframe import add_day_column, add_hour_column, add_return_column, add_2h_sideway_type

def load_candlestick(merchandise_rate_name, interval, limit = 100, start_date = None, end_date = None):
  merchandise_rate = MerchandiseRate()
  merchandise_rate_id = merchandise_rate.find_by_slug(merchandise_rate_name)
  candlestick = Candlestick(merchandise_rate_id, interval=interval, limit=limit, sort="DESC", start_date=start_date, end_date=end_date)

  prices = candlestick.to_df()
  prices = add_return_column(prices)
  prices = add_hour_column(prices)
  prices = add_day_column(prices)
  return prices

def load_data(merchandise_rate_name, interval, limit = 100, start_date = None, end_date = None):
  prices = load_candlestick(merchandise_rate_name, interval, limit, start_date, end_date)

  return prices


def load_data_2h(merchandise_rate_name, interval, limit = 100, start_date = None, end_date = None):
  prices = load_candlestick(merchandise_rate_name, interval, limit, start_date, end_date)
  prices = add_2h_sideway_type(prices)

  prices = prices[prices['hour'].isin([1,2,3,4,5,6,7]) & prices['2h_type'] == True]

  return prices
