import streamlit as st
import numpy as np
import plotly.figure_factory as ff
from hydralit_custom import HydraHeadApp
from apps.helpers.constants import CONFIG
from apps.helpers.draw_chart import draw_candlestick_day_session, draw_candlestick, draw_candlestick_with_highest_and_lowest_zone
from apps.concern.load_data import load_data, load_hour_data
from apps.helpers.datetime_helper import previous_day, day_week_name, date_with_name

class DaySessionApp(HydraHeadApp):
  def __init__(self, title = 'Hydralit Explorer', **kwargs):
    self.__dict__.update(kwargs)
    self.title = title

  def run(self):
    alt_name = 'LTCUSDT'

    day = st.number_input('Nhập số lượng dữ liệu (đơn vị: ngày)', value=50)

    hour_prices = load_hour_data(alt_name, day*24)
    day_prices = load_data(alt_name, 'day', day)

    if st.button("Show raw data"):
      st.dataframe(hour_prices)

    list_day = day_prices.day.to_list()

    for date in list_day:
        st.write(date_with_name(date))

        hour_prices_by_date = hour_prices[hour_prices['day_with_binance'] == date]
        show_date = day_prices[(day_prices['day'] == date) | (day_prices['day'] == previous_day(date)) | (day_prices['day'] == previous_day(previous_day(date)))]

        c1, c2,c3,c4,c5 = st.columns([16,10,8,14,20])

        st.plotly_chart(draw_candlestick_with_highest_and_lowest_zone(hour_prices_by_date), use_container_width=True, config=CONFIG)
        with c1:
          st.plotly_chart(draw_candlestick_day_session(hour_prices_by_date[(hour_prices_by_date['hour'].isin([7,8,9,10,11,12,13,14]))]), use_container_width=True, config=CONFIG)
        with c2:
          st.plotly_chart(draw_candlestick_day_session(hour_prices_by_date[(hour_prices_by_date['hour'].isin([15,16,17,18,19]))]), use_container_width=True, config=CONFIG)
        with c3:
          st.plotly_chart(draw_candlestick_day_session(hour_prices_by_date[(hour_prices_by_date['hour'].isin([20,21,22,23]))]), use_container_width=True, config=CONFIG)
        with c4:
          st.plotly_chart(draw_candlestick_day_session(hour_prices_by_date[(hour_prices_by_date['hour'].isin([0,1,2,3,4,5,6]))]), use_container_width=True, config=CONFIG)
        with c5:
          st.plotly_chart(draw_candlestick(show_date), use_container_width=True, config=CONFIG)
