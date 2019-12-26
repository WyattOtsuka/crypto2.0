print("Starting...")
import datetime
startingTime = datetime.datetime.now()

import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
import math
print("Started in " + str(datetime.datetime.now() - startingTime))

points = 20000


#parse data into frames for input
bigRawIn = pd.read_csv('data/rawTrades/data_0.csv')
fileIdx = 0
largeDf = []
endTimes = []

for i in range(points):
    if len(bigRawIn) <= 1500:
        fileIdx += 1
        bigRawIn = bigRawIn.append(pd.read_csv('data/rawTrades/data_' + str(fileIdx) + '.csv'), ignore_index = True)
    smallDf = []
    
    for j in range(1500):
        smallDf.append(bigRawIn['price'][j])
    
    endTimes.append(bigRawIn['time'][1499] - bigRawIn['time'][1499] % 1000)
    bigRawIn = bigRawIn.drop(bigRawIn.head(1500).index)
    bigRawIn = bigRawIn.reset_index(drop=True)
    
    largeDf.append(smallDf)

    if i % 25 == 0:
        print("IN Cycle " + str(i) + " done in " + str(datetime.datetime.now() - startingTime))

pd.DataFrame(largeDf).to_csv('train_trades.csv', index = False)
train_trades = np.asarray(largeDf)

#parses data into frames for test answers
bigRawAns = pd.read_csv('data/priceOverTime/pot_0.csv')
fileIdx = 0
largeDf = []

for i in range(points):

    smallDf = []

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
        smallDf.append(bigRawAns['price'][j])


    largeDf.append(smallDf)
    if i % 25 == 0:
        print("ANS Cycle " + str(i) + " done in " + str(datetime.datetime.now() - startingTime))
train_prices = np.asarray(largeDf)
pd.DataFrame(largeDf).to_csv('train_prices.csv', index = False)

print("finished in " + str(datetime.datetime.now() - startingTime))



model = keras.Sequential([
    keras.layers.InputLayer(1500),
    keras.layers.Dense(900, activation = "relu"),
    keras.layers.Dense(600, activation = "linear")
])

model.compile(optimizer = "adam", loss = "mse", metrics = ["accuracy"])

model.fit(train_trades, train_prices, epochs = 8)

model.save('20kmk1.h5')

#test_loss, test_acc = model.evaluate
