with open('text_2_var_74') as file:
    lines = file.readlines()

result = []
for line in lines:
    result.append(sum(int(number) for number in line.split(',')))

with open('text_2_output', 'w') as file:
    for elem in result:
        file.write(str(elem) + '\n')