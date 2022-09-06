import streamlit as st
import datetime as dt
import pandas as pd
# import pandas_profiling
from hydralit import HydraHeadApp
from apps.helpers.draw_chart import draw_simple_barchart
from apps.concern.load_data import load_day_data
from apps.helpers.datetime_helper import next_day, previous_day, to_str, to_date
from apps.helpers.utils import unique_list
from apps.helpers.constants import FIRST_MERCHANDISE_DATE_IN_DB, MID_AUTUMN_DATE


CONFIG = {'displayModeBar': False, 'responsive': False}

class MidAutumnApp(HydraHeadApp):

  def __init__(self, title = 'Hydralit Explorer', **kwargs):
    self.__dict__.update(kwargs)
    self.title = title

  def run(self):
    day = (dt.datetime.now() - to_date(FIRST_MERCHANDISE_DATE_IN_DB['BTCUSDT'])).days + 1

    day_prices = load_day_data('BTCUSDT', day)

    mid_autumn_prices = day_prices[day_prices['day'].isin(MID_AUTUMN_DATE)]

    st.write(mid_autumn_prices)
    st.write(mid_autumn_prices.day.to_list())
    st.write(mid_autumn_prices.day_return.to_list())


    chart_data = pd.DataFrame(
      {'value': mid_autumn_prices.day_return.to_list()},
      columns=mid_autumn_prices.day.to_list())

    st.write(chart_data)

    # st.bar_chart(mid_autumn_prices['day_return'])
    st.bar_chart(chart_data)


    # prices = load_data_2h('DOTUSDT', 'hour', 24*day)

    # prices_2h = prices[prices['hour'].isin([1,2,3,4,5,6,7]) & prices['2h_type'] == True]

    # list_valid_day = unique_list(prices_2h.day.values.tolist())
    # st.plotly_chart(draw_candlestick(prices_2h), use_container_width=True)

    # c1, c2 = st.columns([1, 1])
    # with c1:
    #   date = st.selectbox("Danh sách ngày đủ điều kiện", list_valid_day)
    # with c2:
    #   st.write(f"Số ngày đủ điều kiện là {len(list_valid_day)}/{day}")
    # target_date = st.date_input(
    #     "Chọn ngày",
    #     to_date(date))
    # date = to_str(target_date)

    # c1, c2 = st.columns([48, 20])
    # hour_prices = hour_prices[(hour_prices['day'] == previous_day(date)) | (hour_prices['day'] == date)]

    # date_prices = day_prices[(day_prices['day'] == previous_day(date)) | (day_prices['day'] == date) | (day_prices['day'] == next_day(date))]
    # with c1:
    #   st.plotly_chart(draw_candlestick_2h(hour_prices, date), use_container_width=True, config=CONFIG)
    # with c2:
    #   st.plotly_chart(draw_candlestick(date_prices), use_container_width=True, config=CONFIG)

    # st.write("Return change của 2h")
    # prices_2h_return_list =  prices_2h[prices_2h['hour'] == 2].hour_return

    # st.write(prices_2h_return_list.to_list())

    # st.plotly_chart(draw_histogram(prices_2h_return_list.to_list(), 100))
