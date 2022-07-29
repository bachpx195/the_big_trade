import streamlit as st
# import pandas_profiling
from hydralit import HydraHeadApp
from apps.helpers.draw_chart import draw_candlestick, draw_candlestick_2h
from apps.concern.load_data import load_data_2h, load_data
from apps.helpers.datetime_helper import next_day, previous_day, to_str, to_date
from apps.helpers.utils import unique_list

CONFIG = {'displayModeBar': False, 'responsive': False}

class Data2hApp(HydraHeadApp):

  def __init__(self, title = 'Hydralit Explorer', **kwargs):
    self.__dict__.update(kwargs)
    self.title = title

  def run(self):
    day = st.number_input('Nhập số lượng dữ liệu (đơn vị: ngày)', value=50)
    hour_prices = load_data('DOTUSDT', 'hour', day*24)
    day_prices = load_data('DOTUSDT', 'day', day)

    prices = load_data_2h('DOTUSDT', 'hour', 24*60)

    prices_2h = prices[prices['hour'].isin([1,2,3,4,5,6,7]) & prices['2h_type'] == True]

    list_valid_day = unique_list(prices_2h.day.values.tolist())
    st.plotly_chart(draw_candlestick(prices_2h), use_container_width=True)

    date = st.selectbox("Danh sách ngày đủ điều kiện", list_valid_day)
    target_date = st.date_input(
        "Chọn ngày",
        to_date(date))
    date = to_str(target_date)

    c1, c2 = st.columns([48, 20])
    hour_prices = hour_prices[(hour_prices['day'] == previous_day(date)) | (hour_prices['day'] == date)]

    date_prices = day_prices[(day_prices['day'] == previous_day(date)) | (day_prices['day'] == date) | (day_prices['day'] == next_day(date))]
    with c1:
      st.plotly_chart(draw_candlestick_2h(hour_prices, date), use_container_width=True, config=CONFIG)
    with c2:
      st.plotly_chart(draw_candlestick(date_prices), use_container_width=True, config=CONFIG)
