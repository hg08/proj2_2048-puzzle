import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt


def gen_series(file):
    # read data from csv file
    data = pd.read_csv(file, sep=',')

    return data

data = gen_series('utility.csv')
print(data)
plt.plot(data["10.0"])
plt.plot(data["780"])
plt.plot(data["18"])
plt.show()
