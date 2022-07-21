# update _data/gobos.yml with stock numbers from _stacktake/gobos.txt

from sqlalchemy import null
import yaml
from operator import itemgetter


igobos = {}

def input_gobo(make, code, size, amount):
  if make not in igobos:
    igobos[make] = {}
  if code not in igobos[make]:
    igobos[make][code] = {}
  igobos[make][code][size] = amount

with open('_stocktake/gobos.txt', 'r') as f:
  text = f.read().split('\n\n')

for manufacturer in text:
  if manufacturer != '':
    manufacturer_name = manufacturer.split('\n')[0]
    for line in manufacturer.split('\n')[1:]:
        if line != '':
            amount = line.split(' ')[0][0:-1]
            size = line[-1:].upper()
            code = line.split(' ', 1)
            print(code)
            code = code[1][:-2]
            input_gobo(manufacturer_name, code, size, amount)

with open("_data/gobos.yml", "r") as f:
  ogobos = yaml.load(f, Loader=yaml.Loader)

print("{} gobos to process, processing all known".format(len(igobos)))

for gobo in ogobos:
    make = gobo['make']
    code = gobo['number']
    gobo['stock'] = []
    if make in igobos and code in igobos[make]:
        # In input list, add what we have
        for size, amount in igobos[make][code].items():
            gobo['stock'].append({'size': size, 'qty': amount})

        # Done with gel, pop from dict
        igobos[make].pop(code)
        if len(igobos[make]) == 0:
            igobos.pop(make)
    
print("{} gobos to process, processing unknowns".format(len(igobos)))

for make in igobos:
    for code, sizes in igobos[make].items():
        gobo = {'make': make, 'number': code, 'stock': None}
        stock = []
        for size, amount in sizes.items():
            stock.append({'size': size, 'qty': amount})
            gobo['stock'] = stock

        ogobos.append(gobo)

ogobos = sorted(ogobos, key=lambda x: (-1*str(x['make']), str(x['number'])))

with open("_data/gobos.yml", "w") as f:
  stream = yaml.dump(ogobos, Dumper=yaml.Dumper, width=720, indent=2)
  stream = stream.replace('\n- ', '\n\n- ')
  stream = stream.replace('!!python/unicode ', '')
  f.write(stream)

print("done")