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


#parse data into frames for input
bigRawIn = pd.read_csv('data/rawTrades/data_100.csv')
fileIdx = 0
largeDf = []
endTimes = []

for i in range(10000):
    if len(bigRawIn) < 3000:
        fileIdx += 1
        bigRawIn = pd.read_csv('data/rawTrades/data_' + str(fileIdx) + '.csv')
    smallDf = []
    for j in range(1500):
        smallDf.append(bigRawIn['price'][j])
    endTimes.append(bigRawIn['time'][1499] - bigRawIn['time'][1499] % 1000)
    bigRawIn = bigRawIn.drop(bigRawIn.head(1500).index)
    bigRawIn = bigRawIn.reset_index(drop=True)
    largeDf.append(smallDf)

    if i % 10 == 0:
        print("IN Cycle " + str(i) + " done in " + str(datetime.datetime.now() - startingTime))
train_trades = np.asarray(largeDf)

#parses data into frames for test answers
bigRawAns = pd.read_csv('data/priceOverTime/pot_0.csv')
fileIdx = 0
largeDf = []

for i in range(10000):
    if len(bigRawAns) < 1200:
        fileIdx += 1
        bigRawIn = pd.read_csv('data/rawTrades/data_' + str(fileIdx) + '.csv')
    smallDf = []
    for j in range(600):
        smallDf.append(bigRawAns['price'][j])
    k = (bigRawAns.time.values == endTimes[i]).argmax()
    bigRawAns = bigRawAns.drop(bigRawAns.head(k).index)
    bigRawAns = bigRawAns.reset_index(drop=True)


    largeDf.append(smallDf)
    if i % 10 == 0:
        print("ANS Cycle " + str(i) + " done in " + str(datetime.datetime.now() - startingTime))
train_prices = np.asarray(largeDf)
print(len(train_trades))

print("finished in " + str(datetime.datetime.now() - startingTime))



model = keras.Sequential([
    keras.layers.InputLayer(1500),
    keras.layers.Dense(900, activation = "relu"),
    keras.layers.Dense(600, activation = "linear")
])

model.compile(optimizer = "adam", loss = "mse", metrics = ["accuracy"])

model.fit(train_trades, train_prices, epochs = 5)

#test_loss, test_acc = model.evaluate
