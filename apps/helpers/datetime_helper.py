import datetime
from dateutil.relativedelta import relativedelta

def next_day(date):
  return (to_date(date) + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

def previous_day(date):
  return (to_date(date) - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

def next_month(month):
  date = to_date(f"2020-{month}-01")
  return (date + relativedelta(months=+1)).strftime('%m')

def previous_month(month):
  date = to_date(f"2020-{month}-01")
  return (date - relativedelta(months=+1)).strftime('%m')

def to_date(date_str):
  return datetime.datetime.strptime(date_str, "%Y-%m-%d")

def to_str(date):
  return date.strftime("%Y-%m-%d")

def day_week_name(date_str):
  return to_date(date_str).strftime("%A")

def date_with_name(date_str):
  return to_date(date_str).strftime("%Y-%m-%d %A")
