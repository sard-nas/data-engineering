with open('text_3_var_74') as file:
    lines = file.readlines()

result = []
for line in lines:
    lst = line.split(',')

    for i in range(len(lst)):
        if lst[i] == 'NA':
            lst[i] = (int(lst[i-1]) + int(lst[i+1])) / 2
    
    lst = list(map(int, lst))
    lst = list(filter(lambda x: x ** 0.5 >= (50 + 74), lst))
    if len(lst) > 0:
        result.append(lst)

with open('text_3_output', 'w') as output:
    for line in result:
        output.write(",".join(str(num) for num in line) + '\n')

