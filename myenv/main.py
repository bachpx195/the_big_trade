
from models.candlestick import Candlestick
from models.merchandise_rate import MerchandiseRate

import pandas as pd

candlestick = Candlestick()
merchandise_rate = MerchandiseRate()
merchandise_rate.find_by_slug('BTCUSDT')

df = candlestick.to_df()
print(df)
