import os
import pandas as pd
from plots import *

use_dtypes = read_types('results/task6/dtypes.json')
dataframe = pd.read_csv('results/task6/dataframe.csv',
                      usecols=lambda x: x in use_dtypes.keys(),
                      dtype=use_dtypes)

os.makedirs('plots/task6', exist_ok=True)

#   Scatter plot
scatter_plot(dataframe, 'Vict Sex', 'Vict Age', 'Vict Sex by age', 'plots/task6/1.png')

#   Barplot 1
bar_plot(dataframe, 'Status Desc', 'Vict Age', 'Victim age by crime status', 'plots/task6/2.png')

#   Barplot 2
bar_plot(dataframe, 'Vict Sex', 'Weapon Used Cd', 'Used weapon by victim sex', 'plots/task6/3.png')

#   Pie plot
pie_plot(dataframe['Status'], 'Crime status frequency', 'plots/task6/4.png')

#   Correlation map
correlation_map(dataframe, 'plots/task6/5.png') 