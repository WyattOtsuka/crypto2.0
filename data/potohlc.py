
print('Starting...')
import datetime
t = datetime.datetime.now()
import pandas as pd 
print('Started in ' + str(datetime.datetime.now() - t))

basePath = './rawTrades/data_'
fnum = 821
outNum = 71
idx = 0
df = pd.read_csv(basePath + str(fnum) + '.csv')[161133:].reset_index()

print(df['time'][0])

startTime = 1573942428000
secVol = 0
priceVol = 0
out = []

while fnum < 827:
    while len(out) < 1000000: 
        while idx < len(df) and startTime + 1000 > df['time'][idx]:
            secVol += df['qty'][idx]
            priceVol += df['price'][idx] * df['qty'][idx]
            idx += 1
            

        if secVol == 0:
            if priceVol != 0:
                raise StopIteration
        else:
            price = priceVol / secVol

        row = {'price': price, 'time' : startTime}

        startTime += 1000
        priceVol = 0
        secVol = 0
        out.append(row)
        
        if len(df) < 50000 and fnum < 827:
            fnum += 1
            print('Read from file number' + str(fnum) + '. df now size ' + str(len(df)))
            df = df.append(pd.read_csv(basePath + str(fnum) + '.csv'), ignore_index = True, )
        if idx > 5000:
            print('Dropped indecies. df now size ' + str(len(df)))
            df = df.iloc[idx:,].reset_index(drop = True)
            idx = 0
    dfOut = pd.DataFrame(out)
    fpath = ('priceOverTime/pot_' + str(outNum) + '.csv')
    with open(fpath, 'a') as f:
        dfOut.to_csv(f, index = False)
        print('Printed to file number ' + str(outNum))
    outNum+=1
    out = []
