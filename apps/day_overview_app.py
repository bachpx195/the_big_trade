import streamlit as st
import numpy as np
import plotly.figure_factory as ff
import pandas as pd
from hydralit_custom import HydraHeadApp
from apps.helpers.constants import CONFIG
from apps.helpers.draw_chart import draw_day_overview, draw_candlestick, draw_candlestick_with_highest_and_lowest_zone
from apps.concern.load_data import load_data, load_hour_data
from apps.helpers.datetime_helper import previous_day, day_week_name, date_with_name

class DayOverviewApp(HydraHeadApp):
  def __init__(self, title = 'Hydralit Explorer', **kwargs):
    self.__dict__.update(kwargs)
    self.title = title

  def run(self):
    alt_name = 'LTCUSDT'
    btc_name = 'LTCBTC'

    day = st.number_input('Nhập số lượng dữ liệu (đơn vị: ngày)', value=50)

    hour_prices_alt = load_hour_data(alt_name, day*24)
    day_prices_alt = load_data(alt_name, 'day', day)

    hour_prices_btc = load_hour_data(btc_name, day*24)
    day_prices_btc = load_data(btc_name, 'day', day)

    if st.button("Show raw data"):
      st.dataframe(hour_prices_alt)
      st.dataframe(hour_prices_btc)

    list_day = day_prices_alt.day.to_list()

    for date in list_day:
        hour_prices_alt_by_date = hour_prices_alt[hour_prices_alt['day_with_binance'] == date]
        hour_prices_btc_by_date = hour_prices_btc[hour_prices_btc['day_with_binance'] == date]

        # Nếu không đủ giờ thì ko hiển thị
        if len(hour_prices_alt_by_date) < 24:
          continue

        st.write(date_with_name(date))

        show_date_alt = day_prices_alt[(day_prices_alt['day'] == date) | (day_prices_alt['day'] == previous_day(date)) | (day_prices_alt['day'] == previous_day(previous_day(date)))]

        show_date_btc = day_prices_btc[(day_prices_btc['day'] == date) | (day_prices_btc['day'] == previous_day(
            date)) | (day_prices_btc['day'] == previous_day(previous_day(date)))]


        c1,c2 = st.columns([1,4])

        # Thêm nến ngay hôm trước
        day_ohlc_alt = day_prices_alt[(day_prices_alt['day'] == previous_day(date))].values.tolist()[0]
        day_ohlc_alt.append(day_ohlc_alt[-1])
        day_df_alt = pd.DataFrame([day_ohlc_alt], columns=hour_prices_alt_by_date.columns)
        day_df_alt = day_df_alt.set_index(pd.DatetimeIndex([f"{previous_day(date)} 00:00:00+00:00"]))

        hour_prices_alt_by_date = pd.concat([day_df_alt, hour_prices_alt_by_date])
        hour_prices_alt_by_date.sort_index(inplace=True) 

        # Thêm nến ngay hôm trước
        day_ohlc_btc = day_prices_btc[(
            day_prices_btc['day'] == previous_day(date))].values.tolist()[0]
        day_ohlc_btc.append(day_ohlc_btc[-1])
        day_df_btc = pd.DataFrame(
            [day_ohlc_btc], columns=hour_prices_btc_by_date.columns)
        day_df_btc = day_df_btc.set_index(
            pd.DatetimeIndex([f"{previous_day(date)} 00:00:00+00:00"]))

        hour_prices_btc_by_date = pd.concat(
            [day_df_btc, hour_prices_btc_by_date])
        hour_prices_btc_by_date.sort_index(inplace=True)

        with c1:
          # st.write(alt_name)
          st.plotly_chart(draw_candlestick(show_date_alt), use_container_width=True, config=CONFIG)
        with c2:
          st.plotly_chart(draw_day_overview(hour_prices_alt_by_date, day_df_alt), use_container_width=True, config=CONFIG)

        # with c1:
        #   st.write(btc_name)
        #   st.plotly_chart(draw_candlestick(show_date_btc),
        #                   use_container_width=True, config=CONFIG)
        # with c2:
        #   st.plotly_chart(draw_day_overview(hour_prices_btc_by_date, day_df_btc), use_container_width=True, config=CONFIG)