import os
import pandas as pd
from plots import *

use_dtypes = read_types('results/task3/dtypes.json')
dataframe = pd.read_csv('results/task3/dataframe.csv',
                      usecols=lambda x: x in use_dtypes.keys(),
                      dtype=use_dtypes)

os.makedirs('plots/task3', exist_ok=True)

#   Linear plot
linear_plot(dataframe, 'MONTH', 'AIR_TIME', 'Air time by month', 'plots/task3/1.png')

#   Barplot 1
bar_plot(df=dataframe, x='DAY_OF_WEEK', y='WEATHER_DELAY', title='Weather delay by day of week', filename='plots/task3/2.png')

#   Barplot 2
bar_plot(df=dataframe, x='MONTH', y='WEATHER_DELAY', title='Weather delay by month', filename='plots/task3/3.png')

#   Pie plot 1
pie_plot(dataframe['CANCELLED'], 'Cancelled flights', 'plots/task3/4.png')

#   Correlation map
correlation_map(dataframe, 'plots/task3/5.png')