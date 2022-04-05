import streamlit as st
import datetime
import numpy as np
from hydralit import HydraHeadApp
from apps.helpers.constants import LIST_MERCHANDISE_RATE
from apps.models.candlestick import Candlestick
from apps.models.merchandise_rate import MerchandiseRate
from apps.helpers.constants import HIGH_INDEX, LOW_INDEX, OPEN_INDEX, CLOSE_INDEX
from apps.helpers.utils import percentage_change, candlestick_type, type_continuous, until_now_type, candlestick_type_by_hour
from apps.helpers.draw_chart import draw_candlestick, draw_time_distribution

class HighestHourInDayApp(HydraHeadApp):

  def __init__(self, title = 'Hydralit Explorer', **kwargs):
    self.__dict__.update(kwargs)
    self.title = title

  @st.experimental_memo
  def load_data(self, merchandise_rate_name, limit, start_date, end_date):
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
    prices['return'] = prices['close'].pct_change() * 100
    return prices

  def init_dataframe(self, df):
    df['hour_return'] = percentage_change(df,OPEN_INDEX, CLOSE_INDEX)
    df['day'] = df[['open']].apply(
        lambda x: x.name.strftime("%Y-%m-%d"), axis=1)
    df['hour'] = df[['open']].apply(
        lambda x: x.name.hour, axis=1)
    df['type'] = candlestick_type(df)


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
      prices['return'] = prices['close'].pct_change() * 100
      return prices

    c1, c2 = st.columns([2, 2])
    merchandise_rate = LIST_MERCHANDISE_RATE[0]
    with c1:
      merchandise_rate = st.radio("Chọn loại tiền cần phân tích: ", LIST_MERCHANDISE_RATE)

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

    prices = load_data(merchandise_rate, record_limit, start_date, end_date)
    self.init_dataframe(prices)

    st.pyplot(draw_time_distribution(prices))

    current_hour = datetime.datetime.now().hour

    hour_observe = st.radio("Chọn giờ quan sát", np.arange(24), index=current_hour)

    