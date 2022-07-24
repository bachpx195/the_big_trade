import streamlit as st
# import pandas_profiling
from hydralit import HydraHeadApp
from apps.helpers.draw_chart import draw_candlestick
from apps.concern.load_data import load_data_2h
from apps.helpers.datetime_helper import next_day, previous_day

CONFIG = {'displayModeBar': False, 'responsive': False}

class Data2hApp(HydraHeadApp):

  def __init__(self, title = 'Hydralit Explorer', **kwargs):
    self.__dict__.update(kwargs)
    self.title = title

  def run(self):
    prices = load_data_2h('DOTUSDT', 'hour', 24*60)
    st.plotly_chart(draw_candlestick(prices), use_container_width=True)
