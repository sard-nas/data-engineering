import os
import pandas as pd
from plots import *

use_dtypes = read_types('results/task1/dtypes.json')
dataframe = pd.read_csv('results/task1/dataframe.csv',
                      usecols=lambda x: x in use_dtypes.keys(),
                      dtype=use_dtypes)

os.makedirs('plots/task1', exist_ok=True)

#   Linear plot
linear_plot(dataframe, 'v_hits', 'v_doubles', 'Count of doubles by hits', 'plots/task1/1.png')

#   Barplot 1
bar_plot(dataframe, 'v_league', 'v_hits', 'Count of hits by league', 'plots/task1/2.png')

#   Barplot 2
bar_plot(dataframe, 'day_of_week', 'attendance', 'Attendance by day', 'plots/task1/3.png')

#   Pie plot
pie_plot(dataframe['day_night'], 'Count of records by day/night', 'plots/task1/4.png')

#   Correlation map
correlation_map(dataframe, 'plots/task1/5.png')