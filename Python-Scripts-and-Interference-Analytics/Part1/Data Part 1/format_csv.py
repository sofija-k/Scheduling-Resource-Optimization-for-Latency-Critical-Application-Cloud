# change this variable for every csv file
name = 'no_interference4.csv'

with open(name, 'r') as f:
    lines = f.readlines()

lines = [line.replace(' ', '') for line in lines]
lines = [line.replace('\xa0', '') for line in lines]
lines = [line.replace('\ufeff', '') for line in lines]

with open(name, 'w') as f:
    f.writelines(lines)
