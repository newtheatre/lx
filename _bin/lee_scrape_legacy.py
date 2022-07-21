import requests
import yaml
from yaml import Loader, Dumper
from bs4 import BeautifulSoup, element

lee_html = requests.get("http://web.archive.org/web/20210618025008id_/http://leefilters.com/lighting/colour-list.html")

assert lee_html.status_code == 200, "Failed to fetch from leefilters.com"

s = BeautifulSoup(lee_html.text, 'html.parser')

print("**{}**".format(s.title.string))

lee_gels = {}

for ci in s.select('#colorlist')[0].children:
  if type(ci) is element.Tag and "swatch" in ci['class']:

    code = "L" + ci.a.string.lstrip("0")
    color = ci['style'][-6:]
    name = ci.span.strong.text
    description = ci.span.text[len(name):]

    lee_gels[code] = {
      'color': color,
      'name': name,
      'description': description,
    }

print("{} colour refs acquired".format(len(lee_gels)))

with open("_data/gels.yml", "r") as f:
  gdata = yaml.load(f, Loader=Loader)

for gel in gdata:
  if gel['code'] in lee_gels:
    gel['color'] = str(lee_gels[gel['code']]['color'])
    gel['name'] = str(lee_gels[gel['code']]['name'])
    gel['description'] = str(lee_gels[gel['code']]['description'])
  else:
    print("Our {} is not present on leefilters.com".format(gel['code']))

with open("_data/gels.yml", "w") as f:
  stream = yaml.dump(gdata, Dumper=Dumper, width=720, indent=2)
  stream = stream.replace('\n- ', '\n\n- ')
  stream = stream.replace('!!python/unicode ', '')
  f.write(stream)
