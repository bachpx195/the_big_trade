# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc
from dash import html
from myenv.models.candlestick import Candlestick
from myenv.helpers.constants import HIGH_INDEX, LOW_INDEX, OPEN_INDEX, CLOSE_INDEX
from myenv.models.merchandise_rate import MerchandiseRate
from myenv.helpers.utils import percentage_change, candlestick_type, type_continuous


app = dash.Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


merchandise_rate = MerchandiseRate()
merchandise_rate_id = merchandise_rate.find_by_slug('LTCUSDT')
candlestick = Candlestick(merchandise_rate_id, 'week', 100, "DESC")

data_prices = candlestick.to_df()

# data_prices['hour_return'] = percentage_change(data_prices, LOW_INDEX, HIGH_INDEX)
# data_prices['hour_return'] = data_prices['close'].pct_change() * 100
data_prices['week_return'] = percentage_change(data_prices,OPEN_INDEX, CLOSE_INDEX)
data_prices['month'] = data_prices[['open']].apply(
    lambda x: x.name.month, axis=1)
data_prices['year'] = data_prices[['open']].apply(
    lambda x: x.name.year, axis=1)

total = data_prices.iloc[:, 0].count()
last_date = data_prices.iloc[0].name.date()
first_date = data_prices.iloc[-1].name.date()

print(f"Thông tin: {total} hàng từ ngày {first_date} đến {last_date}")
print(data_prices)

data_prices['type'] = candlestick_type(data_prices)

data_prices['type_continuous'] = type_continuous(data_prices, "ASC")

fig = data_prices['week_return'].plot(kind='bar')

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)