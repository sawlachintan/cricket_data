
with open('./README.md', 'r') as f:
    readme = f.readlines()

readme = readme[readme.index('### Game types available <br>\n'):]
readme = readme[4:]

table = list()
for x in readme:
    if x[0] != '|':
        break
    table.append(x)
    
print(table)
table = [x.split('| ') for x in table]

input_list = [table[x][2].strip().lower() for x in range(0, len(table))]
print(input_list)