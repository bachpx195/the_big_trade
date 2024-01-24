from calendar import week
import datetime
import streamlit as st
from hydralit_custom import HydraHeadApp
import numpy as np
from apps.helpers.constants import LIST_MERCHANDISE_RATE, CONFIG
from apps.concern.load_data import load_month_data
from apps.helpers.draw_chart import draw_candlestick, draw_histogram, draw_candlestick_without_hovertext
from apps.helpers.datetime_helper import previous_month

class MonthReturnApp(HydraHeadApp):

  def __init__(self, title = 'Hydralit Explorer', **kwargs):
    self.__dict__.update(kwargs)
    self.title = title

  def month_return_analytic(self, merchandise_rate, month_observe):
    prices = load_month_data(merchandise_rate)

    if st.button("Show raw data"):
      st.dataframe(prices)
      st.write(prices['month_return_ol'].to_list())
      st.write(prices['month_return_ho'].to_list())
      st.plotly_chart(draw_histogram([64, 54, 83, 6, 35, 63, 9, 60, 31, 28, 80, 44, 5, 2, 2, 1, 3, 16, 73, 59, 27, 18, 38, 31, 6, 20, 141, 5, 17, 16, 2, 12, 46, 7, 8, 25, 10, 2, 1, 2, 129, 79, 38, 6, 22, 1, 5, 60, 51, 21, 18, 32, 69, 15, 7, 10, 15, 1, 6, 44, 6, 17, 27, 24, 64, 10, 10], 100))
      # st.plotly_chart(draw_histogram(prices['month_return_ho'].to_list(), 100))


    st.bar_chart(prices[prices['month'] == month_observe]['month_return'])

    year_list = prices["year"].unique()

    for year in year_list:
      st.info(f"Năm {year}:")

      show_month = prices[
        ((prices['month'] == month_observe) & (prices['year'] == year)) |
        ((prices['month'] == previous_month(month_observe)) & (prices['year'] == year)) |
        ((prices['month'] == previous_month(
          previous_month(month_observe))) & (prices['year'] == year)) |
        ((prices['month'] == previous_month(previous_month(
          previous_month(month_observe)))) & (prices['year'] == year)) |
        ((prices['month'] == previous_month(previous_month(previous_month(
            previous_month(month_observe))))) & (prices['year'] == year))
      ]
      if not show_month.empty:
        st.plotly_chart(draw_candlestick_without_hovertext(show_month),
                        use_container_width=True, config=CONFIG)

  def run(self):
    st.write('HI, IM A MONTH RETURN!')

    #config css
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;} </style>', unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)

    c1, c2 = st.columns([2, 2])
    merchandise_rate = LIST_MERCHANDISE_RATE[0]
    with c1:
      merchandise_rate = st.radio("Chọn loại tài sản cần phân tích: ", LIST_MERCHANDISE_RATE)

    st.info(f"Month return theo từng năm")

    current_month = datetime.datetime.now().month
    st.info(current_month)

    month_observe = st.radio(
        "Chọn tháng quan sát", ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"], index=(current_month - 1))

    self.month_return_analytic(merchandise_rate, month_observe)
