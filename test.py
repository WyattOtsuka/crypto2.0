
import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
import math

data = [pd.read_csv('data/rawTrades/data_400.csv')['price'][0:1500]]

ans = np.asarray(pd.read_csv('data/priceOverTime/pot_47.csv')['price'][43586:44186])

model = keras.models.load_model('5kmk2.h5')


predicted = model.predict(np.asarray(data))

data = None
print(ans)

try:
    fig = plt.figure()
    plt.plot(np.asarray(ans), color='black')
    plt.plot(predicted[0], color='blue')
    plt.show()
except Exception as e:
    print (str(e))



