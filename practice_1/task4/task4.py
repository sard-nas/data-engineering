import csv

data = []
sumSalary = 0

with open('text_4_var_74', newline='\n', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=',')

    for row in reader:
        item = {
            'id': int(row[0]),
            'name': row[1] + ' ' + row[2],
            'age': int(row[3]),
            'salary': int(row[4].replace('₽', ''))
        }
        data.append(item)
        sumSalary += item['salary']
    
average = sumSalary / len(data)    
result = filter(lambda item: item['salary'] > average and item['age'] > (25 + 74 % 10) , data)
result = sorted(result, key = lambda item: item['id'])

with open('text_4_output', 'w', encoding='utf-8', newline='\n') as output:
    writer = csv.writer(output,delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for item in result:
        writer.writerow(item.values())