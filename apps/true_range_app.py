import os
import streamlit as st
from hydralit import HydraHeadApp
from apps.helpers.constants import LIST_MERCHANDISE_RATE

class TrueRangeApp(HydraHeadApp):

  def __init__(self, title = 'Hydralit Explorer', **kwargs):
    self.__dict__.update(kwargs)
    self.title = title


  #This one method that must be implemented in order to be used in a Hydralit application.
  #The application must also inherit from the hydrapp class in order to correctly work within Hydralit.
  def run(self):
    st.write('HI, IM A TRUE RANGE!')

    merchandise_rate = LIST_MERCHANDISE_RATE[0]
    merchandise_rate_tuple = st.radio("Chọn loại tiền cần phân tích: ", LIST_MERCHANDISE_RATE)

    if (merchandise_rate_tuple == 'LTC/USDT'):
      merchandise_rate = 'LTC/USDT'
