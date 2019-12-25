
print("Starting...")
import datetime
startingTime = datetime.datetime.now()

import plotly.express as px
import plotly.graph_objects as go

import pandas as pd

#Takes a df data, a starting action, and a minimum difference between buy and sell points
#Returns a df with buy and sell points
#We know the next move is a buy
def getPoints(data, threshold, type):
    
    lastSig = data['price'][0]
    currPoint = data['price'][0]
    sigTime = 0
    buyVal = []
    sellVal = []
    buyTime = []
    sellTime = []
    i = 1
    while i < len(data.index):
        currPoint = data['price'][i]
        if type == 'b' or type == 'buy':
            
            if currPoint < lastSig: #Better Buy point
                lastSig = currPoint
                sigTime = i
            if currPoint > lastSig + threshold: #garunteed Sell point
                buyTime.append(sigTime)
                buyVal.append(lastSig)
                type = 's'
                i = sigTime

        else:
            
            if currPoint > lastSig: #Better Sell point
                lastSig = currPoint
                sigTime = i

            if currPoint < lastSig - threshold: #garunteed Buy point
                sellTime.append(sigTime)
                sellVal.append(lastSig)
                type = 'b'
                i = sigTime
        i += 1

    return {'SellTimes' : sellTime, 'SellVal' : sellVal, 'BuyTimes' : buyTime, 'BuyVal' : buyVal}

#Smooths out the data to a nicer curve
def avgOut(df):
    rowList = [
        {'index' : 0, 'price' : df['price'][0], 'time' : df['time'][0]},
        {'index' : 1, 'price' : df['price'][1], 'time' : df['time'][1]},
        {'index' : 2, 'price' : df['price'][2], 'time' : df['time'][2]}
    ]
    for i in range(3, len(df.index) - 3):
        avg = (df['price'][i - 2] + df['price'][i - 1] + df['price'][i] + df['price'][i + 1] + df['price'][i + 2])/5
        dt = {}
        dt.update({'index' : i, 'price' : avg, 'time' : df.iloc[i]['time']})
        rowList.append(dt)

    rowList.append(
        {'index' : len(df.index) - 3, 'price' : df['price'][len(df.index) - 3], 'time' : df['time'][len(df.index) - 3]}
    )
    rowList.append(
        {'index' : len(df.index) - 2, 'price' : df['price'][len(df.index) - 2], 'time' : df['time'][len(df.index) - 2]}
    )
    rowList.append(
        {'index' : len(df.index) - 1, 'price' : df['price'][len(df.index) - 1], 'time' : df['time'][len(df.index) - 1]}
    )

    avgedOut = pd.DataFrame(rowList) 
    return avgedOut

print("Started in " + str(datetime.datetime.now() - startingTime))

print("Building...")
startingTime = datetime.datetime.now()


df = pd.read_csv('data/priceOverTime/pot_69.csv')
df = df.reset_index(drop = False)
df = df.iloc[0:50000]
df.time = [x/1000 for x in df.time]



print("Built in " + str(datetime.datetime.now() - startingTime))



print("Getting points...")
startingTime = datetime.datetime.now()

avg = avgOut(df)

transactions = getPoints(avg, 1, 'b')

print("Got points in " + str(datetime.datetime.now() - startingTime))

print("Plotting...")
startingTime = datetime.datetime.now()

#avg.to_csv('avg.csv', index = False)

#fig1 = px.line(df, x = 'id', y = 'price', title='og Price over time')


fig = px.line(df, x = 'index', y = 'price', title='Price smoothed with buy and sell points')

fig.add_trace(go.Scatter(x=avg['index'], y=avg['price'],
                    mode='lines',
                    name='Average'))
fig.add_trace(go.Scatter(x=transactions['SellTimes'], y=transactions['SellVal'],
                    mode='markers', name='Sells'))
fig.add_trace(go.Scatter(x=transactions['BuyTimes'], y=transactions['BuyVal'],
                    mode='markers', name='Buys'))

fig.show()
fig.show()
fig.show()
fig.show()
fig.show()

print("Plotted in " + str(datetime.datetime.now() - startingTime))
'''
print('--------------------------------------------------------------------')

print("Running simulation...")
startingTime = datetime.datetime.now()

proPerc = []
profit = 0

miniFrame = df[0:300]
df = df.drop(df.head(300).index)
df = df.reset_index()
miniFrame = miniFrame.reset_index()
avg = avgOut(miniFrame)
transactions = getPoints(avg, 200, 'b')

while len(df) >= 300:
    count = 0
    btc = 0
    usd = 10000
    while count < len(transactions['BuyTimes']) and count < len(transactions['SellTimes']):

        btc = usd / transactions['BuyVal'][int(count / 2)]
        usd = btc * transactions['SellVal'][int((count - 1)/ 2)]
        btc = 0
        count += 1

    if usd != 0:
        profit += usd - 10000
    else:
        profit += usd - avg.iloc[299]['price'] * btc
    proPerc.append(usd/10000 - 1)

    miniFrame = df[0:300]
    df = df.drop(df.head(300).index)
    df = df.reset_index(drop = True)
    miniFrame = miniFrame.reset_index()

    avg = avgOut(miniFrame)
    transactions = getPoints(avg, 5, 'b')

print("Simulation ran in " + str(datetime.datetime.now() - startingTime))
print("Average profit was " + str(sum(proPerc) / len(proPerc) * 100)[0:5] + "%")
print("Profit was " + str(profit))
'''