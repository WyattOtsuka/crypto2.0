###Runs thru the list of all the data and creates new fileIns with the volume of bitcoin in 5 second segments

print('Starting...')
import datetime
t = datetime.datetime.now()
import json
import pandas as pd
import time

print('Started in ' + str(datetime.datetime.now() - t))

df = pd.read_csv('data/data_0.csv')

initTime = df['time'][1]

print (initTime)

fileIn = 0
rowIn = 0
rowOut = 0
fileOut = 0
vol = 0
df = pd.read_csv('data/data_' + str(fileIn) + '.csv')
volDf = pd.DataFrame(columns = ['start', 'end', 'vol'])
while fileIn < 53:
    while initTime - df['time'][rowIn] < 5000:
        vol += df['qty'][rowIn]
        x += 1
        if rowIn == 249999:
            fileIn += 1
            df = pd.read_csv('data/data_' + str(fileIn) + '.csv')
            rowIn = 0
    
    volDf['start'][rowOut] = initTime
    volDf['end'][rowOut] = initTime + 5000
    volDf['vol'][rowOut] = vol

    initTime += 5000


    if rowOut == 249999:
        volDf.to_csv('data/volume/vol_' + str(fileOut) + '.csv', header = True, index = False)
        fileout += 1
        rowOut = 0



    

