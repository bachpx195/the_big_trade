import subprocess

def update_data(merchandise_rate, interval, quote='USDT'):
  base = merchandise_rate.split('USDT')[0]

  cmd = f"cd && cd Projects/daily_trading_journal/ && bundle exec rake db:import_candlestick_data base={base} quote={quote} interval={interval}"
  print(cmd)
  ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  while True:
    line = ps.stdout.readline()
    if not line: break
    print(line)
  o, e = ps.communicate()

  if o: print('Output: ' + o.decode('ascii'))
  if e: print('Error: '  + e.decode('ascii'))
  print('code: ' + str(ps.returncode))

  poll = ps.poll()
  if poll is not None:
    return True

def update_all_data(merchandise_rate):
  print("update month")
  is_updated_month = update_data(merchandise_rate, 'month')
  print("update week")
  is_updated_week = update_data(merchandise_rate, 'week')
  print("update day")
  is_updated_day = update_data(merchandise_rate, 'day')
  print("update hour")
  is_updated_hour = update_data(merchandise_rate, 'hour')
  print("update 15m")
  is_updated_15m = update_data(merchandise_rate, 'm15')

  is_updated_with_btc_quote = True if merchandise_rate == "BTCUSDT" else False
  if merchandise_rate != "BTCUSDT":
    print("update month with BTC quote")
    is_updated_month_btc = update_data(merchandise_rate, 'month', 'BTC')
    print("update week with BTC quote")
    is_updated_week_btc = update_data(merchandise_rate, 'week', 'BTC')
    print("update day with BTC quote")
    is_updated_day_btc = update_data(merchandise_rate, 'day', 'BTC')
    print("update hour with BTC quote")
    is_updated_hour_btc = update_data(merchandise_rate, 'hour', 'BTC')
    is_updated_15m_btc = update_data(merchandise_rate, 'm15', 'BTC')
    is_updated_with_btc_quote = is_updated_month_btc and is_updated_week_btc and is_updated_day_btc and is_updated_hour_btc

  return is_updated_month and is_updated_week and is_updated_day and is_updated_hour and is_updated_with_btc_quote and is_updated_15m and is_updated_15m_btc
