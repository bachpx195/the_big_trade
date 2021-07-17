import pandas as pd
from myenv.database.pymysql_conn import DataBase

db = DataBase()
SQL = "SELECT *  FROM DailyTradingJournal_development.candlesticks  ORDER BY candlesticks.date ASC;"
INTERVAL_HASH = {"day": 1, "week": 2}


class Candlestick:
    def __init__(self, interval="day"):
        self.interval = interval

    def to_df(self):
        sql_query = f"SELECT *  FROM DailyTradingJournal_development.candlesticks WHERE candlesticks.time_type = {INTERVAL_HASH[self.interval]} ORDER BY candlesticks.date ASC;"
        db.cur.execute(sql_query)
        columns = ['date', 'open', 'high', 'close', 'low']
        datas = list(db.cur.fetchall())
        data = [(da[8], da[3], da[4], da[5], da[6])
                for da in datas]
        df = pd.DataFrame(columns=columns, data=data)
        df.set_index('date', inplace=True)
        return df
