import streamlit as st
# import pandas_profiling
from hydralit import HydraHeadApp
from apps.helpers.draw_chart import draw_candlestick
from apps.concern.load_data import load_data
from apps.helpers.datetime_helper import next_day, previous_day

CONFIG = {'displayModeBar': False, 'responsive': False}

class DiffDataApp(HydraHeadApp):

  def __init__(self, title = 'Hydralit Explorer', **kwargs):
    self.__dict__.update(kwargs)
    self.title = title

  def run(self):
    hour_prices = load_data('DOTUSDT', 'hour')
    day_prices = load_data('DOTUSDT', 'day')

    st.write('Đồ thị hiện tại')

    date = "2022-07-23"
    current_hour_prices = hour_prices[(hour_prices['day'] == date) | (hour_prices['day'] == next_day(date))]
    current_date_prices = day_prices[(day_prices['day'] == date) | (day_prices['day'] == previous_day(date)) | (day_prices['day'] == previous_day(previous_day(date)))]
    candlestick_number = len(current_hour_prices)

    if candlestick_number >= 46:
      c1, c2 = st.columns([candlestick_number, 20])
      with c1:
        st.plotly_chart(draw_candlestick(current_hour_prices), use_container_width=True, config=CONFIG)
      with c2:
        st.plotly_chart(draw_candlestick(current_date_prices), use_container_width=True, config=CONFIG)
    else:
      c1, c2 , c3 = st.columns([candlestick_number, 47 - candlestick_number, 20])
      with c1:
        st.plotly_chart(draw_candlestick(current_hour_prices), use_container_width=True, config=CONFIG)
      with c3:
        st.plotly_chart(draw_candlestick(current_date_prices), use_container_width=True, config=CONFIG)


    c1, c2 = st.columns([48, 20])
    diff_date = "2022-07-21"
    diff_hour_prices = hour_prices[(hour_prices['day'] == diff_date) | (hour_prices['day'] == next_day(diff_date))]
    diff_date_prices = day_prices[(day_prices['day'] == diff_date) | (day_prices['day'] == previous_day(diff_date)) | (day_prices['day'] == previous_day(previous_day(diff_date)))]
    with c1:
      st.plotly_chart(draw_candlestick(diff_hour_prices), use_container_width=True, config=CONFIG)
    with c2:
      st.plotly_chart(draw_candlestick(diff_date_prices), use_container_width=True, config=CONFIG)
