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

def linear_plot(df, x, y, title, filename, figsize=(8,6)):
    plt.figure(figsize=figsize)
    plt.title(title)
    sns.lineplot(data=df, x=x, y=y)
    plt.savefig(filename)
    plt.close()

def scatter_plot(df, x, y, title, filename, figsize=(10,8)):
    plt.figure(figsize=figsize)
    plt.title(title)
    sns.scatterplot(data=df, x=x, y=y)
    plt.savefig(filename)
    plt.close()

def bar_plot(df, x, y, title, filename, hue=None, figsize=(10,8)):
    plt.figure(figsize=figsize)
    plt.title(title)
    sns.barplot(data=df, x=x, y=y, hue=hue)
    plt.savefig(filename)
    plt.close()

def pie_plot(data, title, filename, figsize=(8,6)):
    plt.figure(figsize=figsize)
    plt.plot = data.value_counts().plot(kind='pie', title=title, autopct='%1.0f%%')
    plt.axis('off')
    plt.savefig(filename)
    plt.close()

def correlation_map(df, filename, figsize=(20,10)):
    plt.figure(figsize=figsize)
    heatmap = sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='Greens')
    heatmap.set_title('Correlation of numeric data')
    heatmap.get_figure().savefig(filename)
    plt.close()