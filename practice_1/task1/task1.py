with open('text_1_var_74') as file:
    text = file.readlines()

freq = {}
for line in text:
    for elem in ',.!?\n':
        line = line.replace(elem, ' ')

    for word in line.split():
        if word in freq:
            freq[word] += 1
        else:
            freq[word] = 1

with open('text_1_output', 'w') as file:
    for word, frequency in sorted(freq.items(), reverse = True, key = lambda x: x[1]):
        file.write(f"{word}: {frequency}\n")