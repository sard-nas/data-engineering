import pandas as pd
import json, msgpack, pickle, csv
import os

data = pd.read_csv('conditions_COVID.csv', low_memory=False)
data = data[['Year','Month','Condition Group','Condition','Age Group','COVID-19 Deaths','Number of Mentions']]
data = data.rename(columns = {'Condition Group': 'Condition_Group', 'Age Group': 'Age_Group', 'COVID-19 Deaths': 'Deaths','Number of Mentions': 'Number_of_Mentions'})

result = {
    'D_max': int(data['Deaths'].max()),
    'D_min': int(data['Deaths'].min()),
    'D_average': round(data['Deaths'].mean(), 2),
    'D_std': round(data['Deaths'].std(), 4),
    'NoM_max': int(data['Number_of_Mentions'].max()),
    'NoM_min': int(data['Number_of_Mentions'].min()),
    'NoM_average': round(data['Number_of_Mentions'].mean(), 2),
    'NoM_std': round(data['Number_of_Mentions'].std(), 4)
}

condition_stat = dict(data['Condition'].value_counts())
for key, value in condition_stat.items():
    condition_stat[key] = int(value)
result['condition_stat'] = condition_stat

age_stat = dict(data['Age_Group'].value_counts())
for key, value in age_stat.items():
    age_stat[key] = int(value)
result['age_stat'] = age_stat

with open("result.json", "w") as f:
    f.write(json.dumps(result))

with open("result.msgpack", "wb") as f:
    f.write(msgpack.dumps(result))

with open("result.pkl", "wb") as f:
    f.write(pickle.dumps(result))

with open('result.csv', 'w', encoding='utf-8', newline='\n') as f:
    writer = csv.writer(f,delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(result.keys())
    writer.writerow(result.values())

print(f"size of msgpack file: {os.path.getsize('result.msgpack')}")
print(f"size of csv file:     {os.path.getsize('result.csv')}")
print(f"size of pkl file:     {os.path.getsize('result.pkl')}")
print(f"size of json file:    {os.path.getsize('result.json')}")