import json
import pandas as pd

base = './data/priceOverTime/pot_'

df = pd.read_csv(base + str(0) + '.csv')

cumdif = 0

for x in range(1,100000):
    cumdif += abs(df['price'][x] - df['price'][x - 1])
print(cumdif)