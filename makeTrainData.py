print("Starting...")
import datetime
startingTime = datetime.datetime.now()
import sys

import numpy as np
import pandas as pd
import math
print("Started in " + str(datetime.datetime.now() - startingTime))

points = 5000
modCount = str(int(points / 1000)) + 'k'
mk = '2'

#parse data into frames for input
bigRawIn = pd.read_csv('data/rawTrades/data_400.csv')
fileIdx = 0
endTimes = []

for i in range(points):
    df = []
    if len(bigRawIn) <= 1500:
        fileIdx += 1
        bigRawIn = bigRawIn.append(pd.read_csv('data/rawTrades/data_' + str(fileIdx) + '.csv'), ignore_index = True)
        
    for j in range(1500):
        df.append(bigRawIn['price'][j])
        
    endTimes.append(bigRawIn['time'][1499] - bigRawIn['time'][1499] % 1000)
    bigRawIn = bigRawIn.drop(bigRawIn.head(50).index)
    bigRawIn = bigRawIn.reset_index(drop=True)
        

    perc = round(i * 20 / points)
    bar = ''
    for k in range(perc):
        bar = bar + '█'
    for k in range(20-perc):
        bar = bar + '-'

    timeElapsed = datetime.datetime.now() - startingTime

    sys.stdout.write("\r>IN Cycle " + str(i) + " done in " + str(timeElapsed) + '\t[' + bar + ']')
    sys.stdout.flush()
    pd.DataFrame([df]).to_csv('train_trades_' + modCount + '_mk' + mk + '.csv', index = False, mode = 'a')

print('\n')

pd.DataFrame(endTimes).to_csv('train_endtimes_' + modCount + '_mk' + mk + '.csv' )            
bigRawIn = None


#parses data into frames for test answers
bigRawAns = pd.read_csv('data/priceOverTime/pot_47.csv')
bigRawAns = bigRawAns.drop(bigRawAns.head(43570).index).reset_index(drop=True)
fileIdx = 0

for i in range(points):
    df = []

    failed = True
    while failed:
        failed = False
        k = bigRawAns.loc[bigRawAns['time'] == endTimes[i]].index
        if len(k) == 0:
            fileIdx += 1
            bigRawAns = bigRawAns.append(pd.read_csv('data/priceOverTime/pot_' + str(fileIdx) + '.csv'), ignore_index = True)
            failed = True
        else:
            bigRawAns = bigRawAns.drop(bigRawAns.head(math.floor(k[0])).index)
            bigRawAns = bigRawAns.reset_index(drop=True)
    if len(bigRawAns) <= 600:
        fileIdx += 1
        bigRawAns = bigRawAns.append(pd.read_csv('data/priceOverTime/pot_' + str(fileIdx) + '.csv'), sort = False, ignore_index = True)

    
    for j in range(600):
        df.append(bigRawAns['price'][j])

    perc = round(i * 20 / points)
    bar = ''
    for k in range(perc):
        bar = bar + '█'
    for k in range(20-perc):
        bar = bar + '-'

    sys.stdout.write("\rANS Cycle " + str(i) + " done in " + str(datetime.datetime.now() - startingTime) + '\t[' + bar + ']')
    sys.stdout.flush()

    pd.DataFrame([df]).to_csv('train_prices_' + modCount + '_mk' + mk + '.csv', index = False, mode = 'a')

#train_prices = np.asarray(pd.read_csv('train_prices_' + modCount + '_' + mk + '.csv'))

#train_trades = np.asarray(pd.read_csv('train_trades_' + modCount + '_' + mk + '.csv'))

print("\nFinished in " + str(datetime.datetime.now() - startingTime))

