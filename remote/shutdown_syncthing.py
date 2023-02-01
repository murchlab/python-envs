import os
import tomli
import xml.etree.ElementTree as ET
import requests

dir = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(dir, 'configs\config.toml')
with open(config_path, "rb") as f:
        config = tomli.load(f)

syncthing_config_path = os.path.join(dir, 'syncthing\config.xml')
tree = ET.parse(syncthing_config_path)
root = tree.getroot()

port =  config['syncthing']['port']
apikey = root.find('gui').find('apikey').text

url = f'http://localhost:{port}/rest/system/shutdown'
headers = {'X-API-Key': apikey}
response = requests.post(url, headers=headers)
print(response)
