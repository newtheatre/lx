from unittest import result
import requests
import yaml
from yaml import Loader, Dumper
from bs4 import BeautifulSoup, element
import os.path


with open("_data/gobos.yml", "r") as f:
    gdata = yaml.load(f, Loader=Loader)

for gobo in gdata:
    gobo_num = ''.join(str(gobo['number']).split())
    print(gobo_num)
    if not 'name' in gobo:
        filename = ''
        if gobo['make'] == 'Goboland':
        
            # Get gobo information from goboland.com
            goboland_search_url = 'https://www.goboland.com/advanced_search_result.php?keywords=' + gobo_num + '&psearch=products&location=United-Kingdom'
            goboland_html = requests.get(goboland_search_url)
            assert goboland_html.status_code == 200, "Failed to fetch from goboland.com"

            s = BeautifulSoup(goboland_html.text, 'lxml')
            name = s.find('span', {'class' : 'searchLinks'})
            if name is None:
                pass

            gobo['name'] = name.text

            # Get gobo image
            gobo_info = name.parent.parent.parent
            imgurl = 'https://www.goboland.com/' + gobo_info.find('img').get('src')
            filename = 'goboland-' + gobo_num + '.jpg'

            

        elif gobo['make'] == 'Rosco':

            # Get gobo information from rosco.com
            rosco_search_url = 'https://emea.rosco.com/en/products/catalog/gobos?search=' + str(gobo_num)
            rosco_html = requests.get(rosco_search_url)
            assert rosco_html.status_code == 200, "Failed to fetch from rosco.com"

            s = BeautifulSoup(rosco_html.text, 'lxml')
            names = s.find_all('div', {'class' : 'product-item'})
            if names is None:
                pass

            for result in names:
                number = result.find('span', {'class' : 'name'}).text
                if number == gobo_num:
                    name = result.find('span', {'class' : 'text-box'}).text.strip().split('\n')[0]
                    image = result.find('img').get('src')
                    break
            
            gobo['name'] = name

            
            # Get gobo image
            imgurl = 'https://emea.rosco.com/' + image
            filename = 'rosco-' + gobo_num + '.jpg'

        if filename is not '':
            path = 'images/gobos/' + filename
            if not os.path.exists(path):
                with open(path, 'wb') as f:
                    f.write(requests.get(imgurl).content)

            gobo['image'] = filename
            


with open("_data/gobos.yml", "w") as f:
    stream = yaml.dump(gdata, Dumper=Dumper, width=720, indent=2)
    stream = stream.replace('\n- ', '\n\n- ')
    stream = stream.replace('!!python/unicode ', '')
    f.write(stream)
