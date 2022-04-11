import streamlit as st
import datetime
import numpy as np
import plotly.figure_factory as ff
from hydralit import HydraHeadApp
from apps.helpers.constants import LIST_MERCHANDISE_RATE, HOURS_IN_DAY
from apps.models.candlestick import Candlestick
from apps.models.merchandise_rate import MerchandiseRate
from apps.services.ochl_dataframe import add_hour_column, add_return_column, add_type_column, add_day_column, add_type_continue_column, add_highest_in_day_column
from apps.helpers.draw_chart import draw_pie_chart, draw_time_distribution, draw_bar_horizontal_chart
from apps.services.custom_dataframe import custom_highest_hour_dataframe

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

  def analytics_hour(self, df, hour_observe):
    st.info(f"Giờ quan sát: {hour_observe}")
    prices_up = df[(df['hour'] == hour_observe) & (df['type'] == 'up')]
    prices_down = df[(df['hour'] == hour_observe) & (df['type'] == 'down')]

    st.info(f"Tỉ lệ nến xanh và đỏ là {len(prices_up.index)}/{len(prices_down.index)} ~ {round(len(prices_up.index)/len(prices_down.index), 2) if len(prices_down.index) != 0 else len(prices_up.index)}")

    c1, c2 = st.columns([2, 2])
    with c1:
      st.write('Chi tiết nến xanh')
      st.write(prices_up['hour_return'].describe())
      hist_data = [prices_up['hour_return'].values.tolist()]

      group_labels = ['Group 1']

      # Create distplot with custom bin_size
      fig = ff.create_distplot(
              hist_data, group_labels, bin_size=1)

      # Plot!
      st.plotly_chart(fig, use_container_width=True)
    with c2:
      st.write('Chi tiết nến đỏ')
      st.write(prices_down['hour_return'].describe())

    st.write("Biểu đồ % hour return qua từng giờ: ")
    st.bar_chart(df[df['hour'] == hour_observe]['hour_return'])


  def run(self):
    #config css
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;} </style>', unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)

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
      merchandise_rate = st.radio("Chọn loại tài sản cần phân tích: ", LIST_MERCHANDISE_RATE)

    c1, c2, c3, c4, c5 = st.columns([4, 1, 1, 1, 1])
    with c1:
      record_limit = st.number_input('Nhập số lượng dữ liệu (đơn vị: giờ)', value=50*HOURS_IN_DAY)
    with c2:
      if st.checkbox("1 Tuần"):
        record_limit = None
        record_limit = 7*HOURS_IN_DAY
    with c3:
      if st.checkbox("1 Tháng"):
        record_limit = None
        record_limit = 30*HOURS_IN_DAY
    with c4:
      if st.checkbox("3 Tháng"):
        record_limit = None
        record_limit = 100*HOURS_IN_DAY
    with c5:
      if st.checkbox("Tất cả"):
        record_limit = None

    c1, c2 = st.columns([2, 2])
    start_date = None
    with c1:
      if st.checkbox("Ngày bắt đầu phân tích"):
        start_date = st.date_input('Chọn ngày bắt đầu')
      else:
        start_date = None

    end_date = None
    with c2:
      if st.checkbox("Ngày kết thúc phân tích"):
        end_date = st.date_input('Chọn ngày kết thúc')
      else:
        end_date = None

    prices = load_data(merchandise_rate, record_limit, start_date, end_date)

    st.info(f"Dữ liệu được quan sát trong {int(record_limit or len(prices.index))/HOURS_IN_DAY} ngày")
    st.header("Thời gian giao dịch biến động nhất trong ngày")
    highest_hour_df = custom_highest_hour_dataframe(prices)
    c1, c2, c3 = st.columns([6, 1, 4])
    with c1:
      st.pyplot(draw_pie_chart(highest_hour_df.groupby(['highest_in_day']).size()))
    with c2:
      st.write(highest_hour_df.groupby(['highest_in_day']).size())
    with c3:
      st.markdown(f"""
        ### Tổng kết
        + Trong tập dữ liệu 30 ngày của {merchandise_rate}, 21h là thời gian có xác suất biến động cao nhất ~ 16,1%.
        + Các khoảng thời gian có xác suất biến động cao khác là 2h, 6h, 8h.
        + Các khoảng thời gian có biến động nhỏ là 0h, 9h, 12h, 13h, 14h, 15h, 16h, 17h.
        ### Lưu ý
        + Tránh giao dịch vào những khoảng thời gian có xác suất biến động cao.
        + Sau khi xuất hiện giờ biến động cao, thời gian còn lại sẽ giao động hội tụ trong biên độ.
      """)

    st.header("Hiệu ứng thời gian trong ngày")
    c1, c2 = st.columns([7, 4])
    with c1:
      st.pyplot(draw_time_distribution(prices))
    with c2:
      st.markdown(f"""
        ### Tổng kết
        + Trong tập dữ liệu 30 ngày của {merchandise_rate}, 20h là thời gian có xác suất nến xanh cao.
        ### Lưu ý
        + Đặt lệnh mua với các khung giờ có xác suất nến xanh cao, ngược lại đối với lệnh bán.
      """)

    if st.button("Hiện thị tăng/giảm liên tục của cụm nến"):
      c1, c2, c3 = st.columns([6, 1, 4])
      prices = add_type_continue_column(prices)
      type_continuous_group = prices.groupby(['type_continuous']).size()

      with c1:
        st.pyplot(draw_pie_chart(type_continuous_group))
      with c2:
        st.write(type_continuous_group)
      with c3:
        st.markdown(f"""
          ### Tổng kết
          + Trong tập dữ liệu 30 ngày của {merchandise_rate}, 21h là thời gian có xác suất biến động cao nhất ~ 16,1%.
          + Các khoảng thời gian có xác suất biến động cao khác là 2h, 6h, 8h.
          + Các khoảng thời gian có biến động nhỏ là 0h, 9h, 12h, 13h, 14h, 15h, 16h, 17h.
          ### Lưu ý
          + Tránh giao dịch vào những khoảng thời gian có xác suất biến động cao.
          + Sau khi xuất hiện giờ biến động cao, thời gian còn lại sẽ giao động hội tụ trong biên độ.
        """)

    current_hour = datetime.datetime.now().hour
    hour_observe = st.radio("Chọn giờ quan sát", np.arange(24), index=current_hour)
    self.analytics_hour(prices, hour_observe)

    if st.button(f"Hiện thị tăng/giảm liên tục của cụm nến trong {hour_observe}"):
      c1, c2, c3 = st.columns([6, 1, 4])
      type_continuous_str = f"type_continuous_{hour_observe}"
      data_prices_by_hour = prices[(prices['hour'] == hour_observe)]
      data_prices_by_hour = add_type_continue_column(data_prices_by_hour, type_continuous_str)
      type_continuous_group_by_hour = data_prices_by_hour.groupby([type_continuous_str]).size()

      with c1:
        st.pyplot(draw_pie_chart(type_continuous_group_by_hour))
      with c2:
        st.write(type_continuous_group_by_hour)
      with c3:
        st.markdown(f"""
          ### Tổng kết
          + Trong tập dữ liệu 30 ngày của {merchandise_rate}, 21h là thời gian có xác suất biến động cao nhất ~ 16,1%.
          + Các khoảng thời gian có xác suất biến động cao khác là 2h, 6h, 8h.
          + Các khoảng thời gian có biến động nhỏ là 0h, 9h, 12h, 13h, 14h, 15h, 16h, 17h.
          ### Lưu ý
          + Tránh giao dịch vào những khoảng thời gian có xác suất biến động cao.
          + Sau khi xuất hiện giờ biến động cao, thời gian còn lại sẽ giao động hội tụ trong biên độ.
        """)
