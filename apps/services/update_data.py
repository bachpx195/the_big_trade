import subprocess

def update_data():
    cmd = 'cd && cd Projects/daily_trading_journal/ && bundle exec rake db:import_candlestick_data base=LTC quote=USDT interval=month'
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
