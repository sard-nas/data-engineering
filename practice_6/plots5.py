import os
import pandas as pd
from plots import *

use_dtypes = read_types('results/task5/dtypes.json')
dataframe = pd.read_csv('results/task5/dataframe.csv',
                      usecols=lambda x: x in use_dtypes.keys(),
                      dtype=use_dtypes)

os.makedirs('plots/task5', exist_ok=True)

#   Linear plot
linear_plot(dataframe, 'class', 'H', 'Absolute magnitude parameter by class', 'plots/task5/1.png')

#   Scatter plot
scatter_plot(dataframe, 'diameter', 'moid', 'Minimum orbit intersection distance by diameter', 'plots/task5/2.png')

#   Barplot 1
bar_plot(dataframe, 'class', 'albedo', 'Albedo by class', 'plots/task5/3.png', hue='neo')

#   Pie plot
pie_plot(dataframe['neo'], 'Near Earth objects', 'plots/task5/4.png')

#   Correlation map
correlation_map(dataframe, 'plots/task5/5.png') 
