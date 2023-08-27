from calendar import week
import streamlit as st
from hydralit_custom import HydraHeadApp
from apps.helpers.constants import LIST_MERCHANDISE_RATE, LIST_INTERVAL
from apps.concern.load_data import load_day_data, load_week_data
from apps.helpers.draw_chart import draw_inside_and_outside_pie_chart, draw_inside_and_outside_week_bar_chart

class InsideAndOutsideApp(HydraHeadApp):

  def __init__(self, title = 'Hydralit Explorer', **kwargs):
    self.__dict__.update(kwargs)
    self.title = title

  def inside_and_outside_analytic(self, merchandise_rate):
    prices = load_day_data(merchandise_rate)

    total = prices.iloc[:,0].count()
    first_date = prices.iloc[0].name.date()
    last_date = prices.iloc[-1].name.date()

    st.write(f"Tổng số data {total} - từ ngày {first_date} đến ngày {last_date}")

    st.dataframe(prices)

    group_inside_bar_type = prices.groupby(
        'inside_bar_type').inside_bar_type.count()

    labels = 'Trong bien do', 'Ngoai bien do pha dinh day', 'Ngoai bien do pha day', 'Ngoai bien do pha dinh'
    sizes = [group_inside_bar_type.loc[0],
          group_inside_bar_type.loc[1], group_inside_bar_type.loc[2], group_inside_bar_type.loc[3]]
    probability_break_high = '{:.1%}'.format((group_inside_bar_type.loc[3] +
                                          group_inside_bar_type.loc[1])/total)
    probability_break_low = '{:.1%}'.format((group_inside_bar_type.loc[2] +
                                         group_inside_bar_type.loc[1])/total)
    probability_break_both = '{:.1%}'.format(group_inside_bar_type.loc[1]/total)
    probability_inside_day = '{:.1%}'.format(group_inside_bar_type.loc[0]/total)


    c1, c2 = st.columns([2, 2])
    with c1:
        st.pyplot(draw_inside_and_outside_pie_chart(sizes, labels))
    with c2:
        st.write(f"Đối với tập dự liệu giá BTC từ {first_date} đến {last_date}, xác suất của việc mức giá cao nhất bị phá vỡ là {probability_break_high}, mức giá thấp nhất bị phá vỡ là {probability_break_low} và cả hai đỉnh đáy bị phá vỡ là {probability_break_both}.")
        st.write(f"Có ít hơn {probability_inside_day} số ngày là những ngày giao dịch trong biên độ")
    return prices

  def week_analytic(self, merchandise_rate, prices):
    week_prices = load_week_data(merchandise_rate, prices)
    st.dataframe(week_prices)

    group_min_low_in_week = week_prices.groupby(
        'min_low_in_week').min_low_in_week.count()

    group_max_high_in_week = week_prices.groupby(
        'max_high_in_week').max_high_in_week.count()

    group_min_vol_in_week = week_prices.groupby(
        'min_vol_in_week').min_vol_in_week.count()

    group_max_vol_in_week = week_prices.groupby(
        'max_vol_in_week').max_vol_in_week.count()

    n_groups = 7
    min_low_in_week = (
        group_min_low_in_week['Monday'],
        group_min_low_in_week['Tuesday'],
        group_min_low_in_week['Wednesday'],
        group_min_low_in_week['Thursday'],
        group_min_low_in_week['Friday'],
        group_min_low_in_week['Saturday'],
        group_min_low_in_week['Sunday']
    )
    max_high_in_week = (
        group_max_high_in_week['Monday'],
        group_max_high_in_week['Tuesday'],
        group_max_high_in_week['Wednesday'],
        group_max_high_in_week['Thursday'],
        group_max_high_in_week['Friday'],
        group_max_high_in_week['Saturday'],
        group_max_high_in_week['Sunday']
    )
    min_vol_in_week = (
        group_min_vol_in_week['Monday'],
        group_min_vol_in_week['Tuesday'],
        group_min_vol_in_week['Wednesday'],
        group_min_vol_in_week['Thursday'],
        group_min_vol_in_week['Friday'],
        group_min_vol_in_week['Saturday'],
        group_min_vol_in_week['Sunday']
    )
    max_vol_in_week = (
        group_max_vol_in_week['Monday'],
        group_max_vol_in_week['Tuesday'],
        group_max_vol_in_week['Wednesday'],
        group_max_vol_in_week['Thursday'],
        group_max_vol_in_week['Friday'],
        group_max_vol_in_week['Saturday'],
        group_max_vol_in_week['Sunday']
    )
    c1, c2 = st.columns([2,2])
    with c1:
        st.pyplot(draw_inside_and_outside_week_bar_chart(n_groups, max_high_in_week, min_low_in_week))
    with c2:
        st.pyplot(draw_inside_and_outside_week_bar_chart(n_groups, max_vol_in_week, min_vol_in_week))

    return week_prices

  def run(self):
    st.write('HI, IM A INSIDE AND OUTSIDE!')

    #config css
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;} </style>', unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)

    c1, c2 = st.columns([2, 2])
    merchandise_rate = LIST_MERCHANDISE_RATE[0]
    with c1:
      merchandise_rate = st.radio("Chọn loại tài sản cần phân tích: ", LIST_MERCHANDISE_RATE)

    st.info(f"Hiệu ứng inside day và outside day")
    prices = self.inside_and_outside_analytic(merchandise_rate)

    st.info(f"Ngày giao dịch biến động nhất tuần")
    week_prices = self.week_analytic(merchandise_rate, prices)
