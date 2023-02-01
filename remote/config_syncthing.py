import os
import shutil
import tomli
import tomli_w
import xml.etree.ElementTree as ET
import random
import subprocess


dir = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(dir, 'configs\config.toml')
if os.path.isfile(config_path):
    with open(config_path, "rb") as f:
        config = tomli.load(f)
        print(config)
else:
    config = {
        'host': {
            'name': '',
            'id': '',
            'domain-name': ''
        },
        'syncthing': {
            'port': 0
        },
        'jupyter': {
            'port': 0
        },
        'vnc': {
            'port': 0
        },
        'gateways': [],
        'networks': []
    }

# Set ports
if not config['syncthing']['port']:
    config['syncthing']['port'] = random.randint(10000, 65536)

while (not config['jupyter']['port']) or (config['jupyter']['port'] == config['syncthing']['port']):
    config['jupyter']['port'] = random.randint(10000, 65536)

while (not config['vnc']['port']) or (config['vnc']['port'] == config['syncthing']['port']) or (config['vnc']['port'] == config['jupyter']['port']):
    config['vnc']['port'] = random.randint(10000, 65536)

syncthing_config_path = os.path.join(dir, 'syncthing\config.xml')

# Initialize the syncthing config file
syncthing_dir = os.path.join(dir, 'syncthing')
process = subprocess.Popen(f'syncthing generate --home {syncthing_dir}')
process.wait()
tree = ET.parse(syncthing_config_path)
root = tree.getroot()

# Delete the default folder
for child in root:
    if child.tag == "folder":
        root.remove(child)

# Get the sycthing id
host_id = root.find('defaults').find('folder').find('device').attrib['id']
config['host']['id'] = host_id

# Set the sycthing name
for device in root.findall('device'):
    if device.attrib['id'] == host_id:
        if config['host']['name']:
            device.attrib['name'] = config['host']['name']
        else:
            config['host']['name'] = device.attrib['name']
        break

# Set the sycthing gui port
gui_address = root.find('gui').find('address')
gui_address.text = '127.0.0.1:' + str(config['syncthing']['port'])

# Save
save_config = True
if save_config:
    with open(config_path, "wb") as f:
        tomli_w.dump(config, f)
    with open(syncthing_config_path, "wb") as f:
        tree.write(f)

    networks_path = os.path.join(dir, 'networks')
    for network in os.listdir(networks_path):
        network_path = os.path.join(networks_path, network)
        if os.path.isdir(network_path):
            network_config_path = os.path.join(network_path, f'config_{host_id}.toml')
            shutil.copyfile(config_path, network_config_path)
