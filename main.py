import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

temperature_data = pd.read_csv('HourlyTemperature.csv')

df = pd.DataFrame(temperature_data)
print(df[1,1])
print(df)
#x = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23])
#y = df[0,:]
#plt.plot(x,y)
#plt.show()



