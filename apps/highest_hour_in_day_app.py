import streamlit as st
import datetime
import numpy as np
from hydralit import HydraHeadApp
from apps.helpers.constants import LIST_MERCHANDISE_RATE, HOURS_IN_DAY
from apps.models.candlestick import Candlestick
from apps.models.merchandise_rate import MerchandiseRate
from apps.services.ochl_dataframe import add_hour_column, add_return_column, add_type_column, add_day_column
from apps.helpers.draw_chart import draw_candlestick, draw_time_distribution

class HighestHourInDayApp(HydraHeadApp):

  def __init__(self, title = 'Hydralit Explorer', **kwargs):
    self.__dict__.update(kwargs)
    self.title = title

  def init_dataframe(self, df):
    df = add_hour_column(df)
    df = add_return_column(df)
    df = add_day_column(df)
    df = add_type_column(df)
    return df

  #This one method that must be implemented in order to be used in a Hydralit application.
  #The application must also inherit from the hydrapp class in order to correctly work within Hydralit.
  def run(self):
    st.write('HI, IM A DATA HOURS!')

    @st.experimental_memo
    def load_data(merchandise_rate_name, limit, start_date, end_date):
      merchandise_rate = MerchandiseRate()
      merchandise_rate_id = merchandise_rate.find_by_slug(merchandise_rate_name)
      candlestick = Candlestick(
        merchandise_rate_id,
        interval='hour',
        limit=limit,
        sort="DESC",
        start_date=start_date,
        end_date=end_date
      )
      prices = candlestick.to_df()
      prices = self.init_dataframe(prices)
      return prices

    c1, c2 = st.columns([2, 2])
    merchandise_rate = LIST_MERCHANDISE_RATE[0]
    with c1:
      merchandise_rate = st.radio("Chọn loại tiền cần phân tích: ", LIST_MERCHANDISE_RATE)

    c1, c2 = st.columns([4, 1])
    with c1:
      record_limit = st.number_input('Nhập số lượng', value=50*HOURS_IN_DAY)
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

    prices = load_data(merchandise_rate, record_limit, start_date, end_date)

    st.info(f"Thời gian quan sát {record_limit} ngày")
    st.pyplot(draw_time_distribution(prices))

    current_hour = datetime.datetime.now().hour

    #radio hang ngang
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;} </style>', unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)

    hour_observe = st.radio("Chọn giờ quan sát", np.arange(24), index=current_hour)
