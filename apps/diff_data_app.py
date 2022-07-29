import streamlit as st
# import pandas_profiling
from hydralit import HydraHeadApp
from apps.helpers.draw_chart import draw_candlestick, draw_candlestick_diff
from apps.concern.load_data import load_data
from apps.helpers.datetime_helper import next_day, previous_day, to_date, to_str

CONFIG = {'displayModeBar': False, 'responsive': False}

class DiffDataApp(HydraHeadApp):

  def __init__(self, title = 'Hydralit Explorer', **kwargs):
    self.__dict__.update(kwargs)
    self.title = title

  def run(self):
    day = st.number_input('Nhập số lượng dữ liệu (đơn vị: ngày)', value=50)
    hour_prices = load_data('DOTUSDT', 'hour', day*24)
    day_prices = load_data('DOTUSDT', 'day', day)

    date = to_date(hour_prices[0:1].day[0])
    target_date = st.date_input(
        "Ngày hiện tại",
        date)
    date = to_str(target_date)

    current_hour_prices = hour_prices[(hour_prices['day'] == date) | (hour_prices['day'] == next_day(date))]
    current_date_prices = day_prices[(day_prices['day'] == date) | (day_prices['day'] == previous_day(date)) | (day_prices['day'] == previous_day(previous_day(date)))]
    candlestick_number = len(current_hour_prices)

    if candlestick_number >= 34:
      c1, c2 = st.columns([candlestick_number, 20])
      with c1:
        st.plotly_chart(draw_candlestick_diff(current_hour_prices), use_container_width=True, config=CONFIG)
      with c2:
        st.plotly_chart(draw_candlestick(current_date_prices), use_container_width=True, config=CONFIG)
    else:
      c1, c2 , c3 = st.columns([candlestick_number, 37 - candlestick_number, 16])
      with c1:
        st.plotly_chart(draw_candlestick_diff(current_hour_prices), use_container_width=True, config=CONFIG)
      with c3:
        st.plotly_chart(draw_candlestick(current_date_prices), use_container_width=True, config=CONFIG)


    diff_date = to_date(day_prices[1:2].day[0])
    target_diff_date = st.date_input(
        "Ngày so sánh",
        diff_date)
    diff_date = to_str(target_diff_date)


    c1, c2 = st.columns([48, 20])
    diff_hour_prices = hour_prices[(hour_prices['day'] == diff_date) | (hour_prices['day'] == next_day(diff_date))]

    diff_date_prices = day_prices[(day_prices['day'] == diff_date) | (day_prices['day'] == previous_day(diff_date)) | (day_prices['day'] == previous_day(previous_day(diff_date)))]
    with c1:
      st.plotly_chart(draw_candlestick_diff(diff_hour_prices), use_container_width=True, config=CONFIG)
    with c2:
      st.plotly_chart(draw_candlestick(diff_date_prices), use_container_width=True, config=CONFIG)
