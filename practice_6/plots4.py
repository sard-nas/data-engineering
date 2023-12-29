import os
import pandas as pd
from plots import *

use_dtypes = read_types('results/task4/dtypes.json')
dataframe = pd.read_csv('results/task4/dataframe.csv',
                      usecols=lambda x: x in use_dtypes.keys(),
                      dtype=use_dtypes)

os.makedirs('plots/task4', exist_ok=True)

#   Linear plot
linear_plot(dataframe, 'type_name', 'salary_from', 'Salary by job type', 'plots/task4/1.png')

#   Barplot 1
bar_plot(dataframe, 'schedule_name', 'salary_from', 'Salary by schedule type', 'plots/task4/2.png')

#   Barplot 1
bar_plot(dataframe, 'schedule_name', 'salary_to', 'Upper bound of salary by schedule type', 'plots/task4/3.png', hue='test_required')

#   Pie plot 1
pie_plot(dataframe['schedule_name'], 'Schedule types', 'plots/task4/4.png')

#   Correlation map
correlation_map(dataframe, 'plots/task4/5.png') 
