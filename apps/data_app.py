import streamlit as st
# import pandas_profiling
from hydralit_custom import HydraHeadApp
from apps.helpers.constants import LIST_MERCHANDISE_RATE, LIST_INTERVAL
from apps.services.update_data import update_all_data
from apps.helpers.draw_chart import draw_candlestick
from apps.concern.load_data import load_data

class DataApp(HydraHeadApp):

  def __init__(self, title = 'Hydralit Explorer', **kwargs):
    self.__dict__.update(kwargs)
    self.title = title

  #This one method that must be implemented in order to be used in a Hydralit application.
  #The application must also inherit from the hydrapp class in order to correctly work within Hydralit.
  def run(self):
    st.write('HI, IM A DATA!')

    c1, c2 = st.columns([2, 2])
    merchandise_rate = LIST_MERCHANDISE_RATE[0]
    with c1:
      merchandise_rate = st.radio("Chọn loại tiền cần phân tích: ", LIST_MERCHANDISE_RATE)

    interval = tuple(LIST_INTERVAL.values())[0]
    with c2:
      interval_tuple = st.radio("Chọn loại thời gian: ", tuple(LIST_INTERVAL.values()))
      for k,v in LIST_INTERVAL.items():
        if v == interval_tuple:
          interval = k

    if st.button('Cập nhật dữ liệu'):
      is_updated = update_all_data(merchandise_rate)
      if is_updated:
        st.write("Cập nhật thành công")


    c1, c2 = st.columns([4, 1])
    with c1:
      record_limit = st.number_input('Nhập số lượng', value=50)
    with c2:
      if st.checkbox("Tất cả"):
        record_limit = None

    c1, c2 = st.columns([2, 2])
    start_date = None
    with c1:
      if st.checkbox("Ngày bắt đầu"):
        start_date = st.date_input('Chọn ngày bắt đầu')
      else:
        start_date = None

    end_date = None
    with c2:
      if st.checkbox("Ngày kết thúc"):
        end_date = st.date_input('Chọn ngày kết thúc')
      else:
        end_date = None

    prices = load_data(merchandise_rate, interval, record_limit, start_date, end_date)
    if st.button('hiển thị dataframe'):
      st.write(prices)
    draw_candlestick(prices)

    st.plotly_chart(draw_candlestick(prices), use_container_width=True)
