print('Starting...')
import datetime
t = datetime.datetime.now()
import requests
import json
import pandas as pd
import time

#key = 'HLFDoUxARIZ5DVD6MwBkuXucwbW6rrESAHhBFlYY6frI7ssx1IrzXkiFZeWmwHVx'
#secret key = 'u8N8QikvAj1qcCdHGmGVO8HtoZK4VmNgOC7nAsf278xavkX1pMGcI6X8xTrPurGU'

print('Started in ' + str(datetime.datetime.now() - t))
base = 'http://binance.com'

id = 197750000

filecount = 791
peak = 0

for x in range (500):
    fpath = ('data_' + str(filecount) + '.csv')
    with open(fpath, 'a') as f:
        for y in range (500):
            r = requests.get(base + '/api/v3/historicalTrades',
                params = {
                    "symbol" : "BTCUSDT",
                    "fromId" : id
                },
                headers = {
                    'X-MBX-APIKEY' : 'HLFDoUxARIZ5DVD6MwBkuXucwbW6rrESAHhBFlYY6frI7ssx1IrzXkiFZeWmwHVx'
                }
            )
            if r.status_code == 429:
                print(r.headers)
                raise StopIteration
            elif r.status_code == 418:
                print("banned!")
                print(r.headers)
                raise StopIteration
            elif r.status_code == 200:
                df = pd.DataFrame(json.loads(r.content))
                id = int(df['id'][499]) + 1
                df.to_csv(f, header = y == 0, index = False)
            if peak < int(r.headers['X-MBX-USED-WEIGHT']):
                peak = int(r.headers['X-MBX-USED-WEIGHT'])
            print('Code: ' + str(r.status_code) + '\tWeight: ' + str(r.headers['X-MBX-USED-WEIGHT']) +
                '\tPeak: ' + str(peak) + '\tTime Elapsed: ' + str(datetime.datetime.now() - t))
    filecount += 1
print(r.headers)
print(df)
