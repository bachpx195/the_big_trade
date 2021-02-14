import pymysql
import pandas as pd

import json


class DataBase:
    def __init__(self):
        mysql_config = self._init_from_json("config/pymysql.json")
        self.host = mysql_config["host"]
        self.port = mysql_config["port"]
        self.db = mysql_config["db"]
        self.user = mysql_config["user"]
        self.password = mysql_config["password"]
        self.autocommit = True
        self.charset = mysql_config["charset"]

        self.con = None
        self.cur = None

        self._connect()

    def _init_from_json(self, path):
        with open(path) as f:
            mysql_config = json.load(f)
        return mysql_config

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
