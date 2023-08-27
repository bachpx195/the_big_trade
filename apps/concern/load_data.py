import streamlit as st
from myenv.models.candlestick import Candlestick
from myenv.models.merchandise_rate import MerchandiseRate
from apps.services.ochl_dataframe import *

@st.cache_data
def load_candlestick(merchandise_rate_name, interval, limit, start_date = None, end_date = None):
  merchandise_rate = MerchandiseRate()
  merchandise_rate_id = merchandise_rate.find_by_slug(merchandise_rate_name)
  candlestick = Candlestick(merchandise_rate_id, interval=interval, limit=limit, sort="DESC", start_date=start_date, end_date=end_date)

  prices = candlestick.to_df()
  prices = add_return_column(prices)
  prices = add_hour_column(prices)
  prices = add_day_column(prices)
  return prices

@st.cache_data
def load_data(merchandise_rate_name, interval, limit, start_date = None, end_date = None):
  prices = load_candlestick(merchandise_rate_name, interval, limit, start_date, end_date)

  return prices

@st.cache_data
def load_hour_data(merchandise_rate_name, limit, start_date = None, end_date = None):
  merchandise_rate = MerchandiseRate()
  merchandise_rate_id = merchandise_rate.find_by_slug(merchandise_rate_name)
  candlestick = Candlestick(merchandise_rate_id, 'hour', limit=limit, sort="DESC", start_date=start_date, end_date=end_date)

  prices = candlestick.to_df()
  prices = add_return_column(prices)
  prices = add_hour_column(prices)
  prices = add_day_column(prices)
  prices = add_day_with_binance_column(prices)
  return prices

@st.cache_data
def load_data_2h(merchandise_rate_name, interval, limit, start_date = None, end_date = None):
  prices = load_candlestick(merchandise_rate_name, interval, limit, start_date, end_date)
  prices = add_2h_sideway_type(prices)

  return prices

@st.cache_data
def load_day_data(merchandise_rate_name, limit=None, start_date = None, end_date = None):
  merchandise_rate = MerchandiseRate()
  merchandise_rate_id = merchandise_rate.find_by_slug(merchandise_rate_name)
  candlestick = Candlestick(merchandise_rate_id, 'day', limit=limit, sort="DESC", start_date=start_date, end_date=end_date)

  prices = candlestick.to_df()
  prices = add_day_return_column(prices)
  prices = add_day_volatility_column(prices)
  prices = add_day_name_column(prices)
  prices = add_day_column(prices)
  prices = add_inside_bar_type_column(prices)

  return prices

@st.cache_data
def load_week_data(merchandise_rate_name, df_day):
  merchandise_rate = MerchandiseRate()
  merchandise_rate_id = merchandise_rate.find_by_slug(merchandise_rate_name)
  candlestick = Candlestick(merchandise_rate_id, interval="week")

  prices = candlestick.to_df()
  prices = add_end_week_column(prices)
  prices = add_min_low_in_week_column(prices, df_day)
  prices = add_max_high_in_week_column(prices, df_day)
  prices = add_min_vol_in_week_column(prices, df_day)
  prices = add_max_vol_in_week_column(prices, df_day)

  return prices


@st.cache_data
def load_month_data(merchandise_rate_name):
  merchandise_rate = MerchandiseRate()
  merchandise_rate_id = merchandise_rate.find_by_slug(merchandise_rate_name)
  candlestick = Candlestick(merchandise_rate_id, interval="month")

  prices = candlestick.to_df()
  prices = add_month_column(prices)
  prices = add_year_column(prices)
  prices = add_month_return_column(prices)

  return prices
