from calendar import week
import streamlit as st
from hydralit import HydraHeadApp
from apps.helpers.constants import LIST_MERCHANDISE_RATE, LIST_INTERVAL
from apps.concern.load_data import load_month_data
from apps.helpers.draw_chart import draw_inside_and_outside_pie_chart, draw_inside_and_outside_week_bar_chart

class MonthReturnApp(HydraHeadApp):

  def __init__(self, title = 'Hydralit Explorer', **kwargs):
    self.__dict__.update(kwargs)
    self.title = title

  def month_return_analytic(self, merchandise_rate):
    prices = load_month_data(merchandise_rate)
    st.bar_chart(prices[prices['month'] == "05"]['month_return'])

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

    self.month_return_analytic(merchandise_rate)
