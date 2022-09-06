import os
import streamlit as st
from hydralit import HydraHeadApp
from apps.concern.load_data import load_data
from apps.helpers.draw_chart import draw_candlestick

MENU_LAYOUT = [1,1,1,7,2]
CONFIG = {'displayModeBar': False, 'responsive': False}

class HomeApp(HydraHeadApp):


   def __init__(self, title = 'Hydralit Explorer', **kwargs):
      self.__dict__.update(kwargs)
      self.title = title


   #This one method that must be implemented in order to be used in a Hydralit application.
   #The application must also inherit from the hydrapp class in order to correctly work within Hydralit.
   def run(self):
      st.write('HI, IM A TRADER!')

      if st.button("Bắt đầu phân tích"):
         alt_name = 'DOTUSDT'
         btc_name = 'BTCUSDT'
         altbtc_name = 'DOTBTC'

         day = st.number_input('Nhập số lượng dữ liệu (đơn vị: ngày)', value=50)

         alt_hour_prices = load_data(alt_name, 'hour', day*24)
         alt_day_prices = load_data(alt_name, 'day', day)
         alt_15m_prices = load_data(alt_name, '15m', day*24*4)

         btc_hour_prices = load_data(btc_name, 'hour', day*24)
         btc_day_prices = load_data(btc_name, 'day', day)
         btc_15m_prices = load_data(btc_name, '15m', day*24*4)

         altbtc_hour_prices = load_data(altbtc_name, 'hour', day*24)
         altbtc_day_prices = load_data(altbtc_name, 'day', day)
         altbtc_15m_prices = load_data(altbtc_name, '15m', day*24*4)

         c1, c2, c3 = st.columns([1, 1, 1])
         with c1:
            st.plotly_chart(draw_candlestick(alt_15m_prices), use_container_width=True, config=CONFIG)
         with c2:
            st.plotly_chart(draw_candlestick(altbtc_15m_prices), use_container_width=True, config=CONFIG)
         with c3:
            st.plotly_chart(draw_candlestick(btc_15m_prices), use_container_width=True, config=CONFIG)

         c1, c2, c3 = st.columns([1, 1, 1])
         with c1:
            st.plotly_chart(draw_candlestick(alt_hour_prices), use_container_width=True, config=CONFIG)
         with c2:
            st.plotly_chart(draw_candlestick(altbtc_hour_prices), use_container_width=True, config=CONFIG)
         with c3:
            st.plotly_chart(draw_candlestick(btc_hour_prices), use_container_width=True, config=CONFIG)
