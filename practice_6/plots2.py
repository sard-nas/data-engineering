import os
import pandas as pd
from plots import *

use_dtypes = read_types('results/task2/dtypes.json')
dataframe = pd.read_csv('results/task2/dataframe.csv',
                      usecols=lambda x: x in use_dtypes.keys(),
                      dtype=use_dtypes)

os.makedirs('plots/task2', exist_ok=True)


#   Scatter plot
df_plot = dataframe[(dataframe['mileage'] < 2_000_000) & (dataframe['askPrice'] < 10_000_000)]
scatter_plot(df_plot, 'mileage', 'askPrice', 'Price by mileage', 'plots/task2/1.png') 

#   Barplot
bar_plot(dataframe, 'vf_FuelTypePrimary', 'askPrice', 'Price by fuel type', 'plots/task2/2.png', figsize=(22,8)) 

#   Linear plot
linear_plot(dataframe, 'vf_FuelTypeSecondary', 'askPrice', 'Price by secondary fuel type', 'plots/task2/3.png', figsize=(22,6)) 

#   Pie plot 1
pie_plot(dataframe['vf_FuelTypeSecondary'], 'Secondary fuel types frequency', 'plots/task2/4.png')

#   Pie plot 2
pie_plot(dataframe['isNew'], 'New cars', 'plots/task2/5.png')

