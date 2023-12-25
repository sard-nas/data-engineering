import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def read_types(filename):
    with open(filename) as file:
        dtypes = json.load(file)

    for key in dtypes.keys():
        if dtypes[key] == 'category':
            dtypes[key] = pd.CategoricalDtype
        else:
            dtypes[key] = np.dtype(dtypes[key])

    return dtypes

use_dtypes = read_types('dtypes.json')
dataset = pd.read_csv('dataframe.csv',
                      usecols=lambda x: x in use_dtypes.keys(),
                      dtype=use_dtypes)

#   Linear plot
plt.title('Count of doubles by hits')
sns.lineplot(x=dataset['v_hits'], y=dataset['v_doubles'])
plt.savefig(f'plots/1.png')
plt.close()

#   Barplot 1
plt.title('Count of hits by league')
sns.barplot(x=dataset['v_league'], y=dataset['v_hits'])
plt.savefig(f'plots/2.png')
plt.close()

#   Barplot 2
plt.title('Attendance by day')
sns.barplot(x=dataset['day_of_week'], y=dataset['attendance'], hue=dataset['day_night'])
plt.savefig(f'plots/3.png')
plt.close()

#   Pie plot
plt.plot = dataset['day_night'].value_counts().plot(kind='pie', title='Count of records' ,autopct='%1.0f%%')
plt.savefig(f'plots/4.png')
plt.close()

#   Correlation map
plt.figure(figsize=(16,8))
heatmap = sns.heatmap(dataset.corr(numeric_only=True), annot=True, cmap='Greens')
heatmap.set_title('Correlation of numeric data')
heatmap.get_figure().savefig('plots/5.png')
plt.close()