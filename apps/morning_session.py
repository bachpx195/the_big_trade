import streamlit as st
import numpy as np
import plotly.figure_factory as ff
from hydralit import HydraHeadApp
from apps.helpers.constants import CONFIG
from apps.helpers.draw_chart import draw_candlestick_morning_session, draw_candlestick
from apps.concern.load_data import load_data
from apps.helpers.datetime_helper import previous_day, day_week_name

class MorningSession(HydraHeadApp):
  def __init__(self, title = 'Hydralit Explorer', **kwargs):
    self.__dict__.update(kwargs)
    self.title = title

  def run(self):
    alt_name = 'LTCUSDT'

    day = st.number_input('Nhập số lượng dữ liệu (đơn vị: ngày)', value=50)

    hour_prices = load_data(alt_name, 'hour', day*24)
    day_prices = load_data(alt_name, 'day', day)

    list_day = day_prices.day.to_list()

    for date in list_day:
        st.write(date)
        st.write(day_week_name(date))

        hour_prices_by_date = hour_prices[(hour_prices['day'] == previous_day(date)) | (hour_prices['day'] == date)]
        show_date = day_prices[(day_prices['day'] == date) | (day_prices['day'] == previous_day(date)) | (day_prices['day'] == previous_day(previous_day(date)))]

        c1, c2 = st.columns([48, 20])
        with c1:
          st.plotly_chart(draw_candlestick_morning_session(hour_prices_by_date), use_container_width=True, config=CONFIG)
        with c2:
          st.plotly_chart(draw_candlestick(show_date), use_container_width=True, config=CONFIG)
