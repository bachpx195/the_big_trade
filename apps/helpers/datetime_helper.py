import datetime

def next_day(date):
  return (to_date(date) + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

def previous_day(date):
  return (to_date(date) - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

def to_date(date):
  return datetime.datetime.strptime(date, "%Y-%m-%d")

def to_str(date):
  return date.strftime("%Y-%m-%d")
