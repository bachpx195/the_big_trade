import pandas as pd
import pytz
from datetime import timezone
from myenv.database.pymysql_conn import DataBase


db = DataBase()
INTERVAL_HASH = {"day": 1, "week": 2, "month": 3, "hour": 4}


class Candlestick:
    def __init__(self, merchandise_rate_id, interval="day", limit=None, sort="ASC", start_date=None, end_date=None):
        self.limit = limit if limit else 100000
        self.interval = interval
        self.merchandise_rate_id = merchandise_rate_id
        self.sort = sort
        self.start_date = start_date
        self.end_date = end_date

    def to_df(self):
        sql_query = 'SELECT * FROM DailyTradingJournal_development.candlesticks WHERE '
        if self.start_date and self.end_date:
            sql_query = sql_query + f"(date BETWEEN '{self.start_date} 00:00:00' AND '{self.end_date} 23:59:59') AND "
        if self.interval:
            sql_query = sql_query + f"candlesticks.time_type = {INTERVAL_HASH[self.interval]} AND "
        if self.merchandise_rate_id:
            sql_query = sql_query + f"candlesticks.merchandise_rate_id = {self.merchandise_rate_id} "
        if self.sort:
            sql_query = sql_query + f"ORDER BY candlesticks.date {self.sort} "
        if self.limit:
            sql_query = sql_query + f"lIMIT {self.limit}"
        sql_query = sql_query + ';'

        db.cur.execute(sql_query)
        columns = ['date', 'open', 'high', 'close', 'low', 'volumn']
        datas = list(db.cur.fetchall())
        data = [(da[8], da[3], da[4], da[5], da[6], da[9])
                for da in datas]
        df = pd.DataFrame(columns=columns, data=data)
        df['date'] = df['date'].dt.tz_localize(timezone.utc)
        my_timezone = pytz.timezone('Asia/Bangkok')
        df['date'] = df['date'].dt.tz_convert(my_timezone)
        df.set_index('date', inplace=True)
        return df
