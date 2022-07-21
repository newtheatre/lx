import csv
import yaml
from yaml import Loader, Dumper

igels = {}

def input_colour(code, result, mode='cut'):
  if code != '':
    if code not in igels:
      igels[code] = {}
    igels[code][mode] = result

# Do cut
with open('_stocktake/cut.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
      input_colour(row['none'], 'none')
      input_colour(row['some'], 'some')
      input_colour(row['many'], 'many')

# Load in sheets
sheets = {}
with open('_stocktake/sheet.csv') as f:
  reader = csv.reader(f)
  for row in reader:
    if row[0] in sheets:
      sheets[row[0]] += 1
    else:
      sheets[row[0]] = 1

# Do sheets
for code, qty in sheets.items():
  input_colour(code, qty, 'sheet')

with open("_data/gels.yml", "r") as f:
  ogels = yaml.load(f, Loader=Loader)

print("{} gels to process, processing all known".format(len(igels)))

for ogel in ogels:
  code = ogel['code']
  if code in igels:
    # In input list, add what we have
    if 'cut' in igels[code]:
      ogel['stock']['cut'] = igels[code]['cut']
    else:
      ogel['stock']['cut'] = 'none'
    if 'sheet' in igels[code]:
      ogel['stock']['sheet'] = igels[code]['sheet']
    else:
      ogel['stock']['sheet'] = 0
    # Done with gel, pop from dict
    igels.pop(code)
  else:
    # Not in input list, we have none
    ogel['stock']['cut'] = 'none'
    ogel['stock']['sheet'] = 0

print("{} gels to process, processing unknowns".format(len(igels)))

if len(igels) > 0:
  print("Gels not known to the catalogue exist! Scrape or manually add data afterwards.")

for code, stock in igels.items():
  if 'cut' not in stock:
    stock['cut'] = 'none'
  if 'sheet' not in stock:
    stock['sheet'] = 0

  ogels.append({
    'code': code,
    'stock': {
      'cut': stock['cut'],
      'sheet': stock['sheet'],
    },
  })

with open("_data/gels.yml", "w") as f:
  stream = yaml.dump(ogels, Dumper=Dumper, width=720, indent=2)
  stream = stream.replace('\n- ', '\n\n- ')
  stream = stream.replace('!!python/unicode ', '')
  f.write(stream)

print("done")

