
from models.candlestick import Candlestick
import pandas as pd

candlestick = Candlestick()

df = candlestick.to_df()
print(df)
