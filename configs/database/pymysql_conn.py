import pymysql
import pandas as pd

import json


class DataBase:
    def __init__(self):
        self.host = "localhost"
        self.port = 3306
        self.db = "DailyTradingJournal_development"
        self.user = "root"
        self.password = "quachtinh95"
        self.autocommit = True
        self.charset = "utf8mb4"

        self.con = None
        self.cur = None

        self._connect()

    def _connect(self):
        if (self.con is not None) or (self.cur is not None):
            return
        self.con = pymysql.connect(host=self.host, port=self.port, db=self.db,
                                   user=self.user, password=self.password,
                                   charset=self.charset, autocommit=self.autocommit)
        self.cur = self.con.cursor()

    def to_df(self, SQL):
        self.cur.execute(SQL)
        columns = [c[0] for c in self.cur.description]
        data = list(self.cur.fetchall())
        df = pd.DataFrame(columns=columns, data=data)
        return df
