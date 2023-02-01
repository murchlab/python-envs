import os
import shutil
import tomli
import tomli_w
import xml.etree.ElementTree as ET
import random
import subprocess
import copy


dir = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(dir, 'configs\config.toml')
with open(config_path, "rb") as f:
    config = tomli.load(f)

if not config['host']['domain-name']:
    gateway_dict = {}
    for gateway in config['gateways']:
        gateway_dict[gateway['name']] = {'id': gateway['id'], 'domain-name': gateway['domain-name']}

    networks_path = os.path.join(dir, 'networks')
    for network in config['networks']:
        network_path = os.path.join(networks_path, network['name'])
        if not os.path.exists(network_path):
            os.makedirs(network_path)
        rathole_configs_path = os.path.join(network_path, 'rathole-configs')
        if not os.path.exists(rathole_configs_path):
            os.makedirs(rathole_configs_path)
        for gateway in network['gateways']:
            rathole_gateway_path = os.path.join(rathole_configs_path, gateway)
            if not os.path.exists(rathole_gateway_path):
                os.makedirs(rathole_gateway_path)
            gateway_config_path = os.path.join(network_path, f"remote-configs\{gateway_dict[gateway]['id']}.toml")
            with open(gateway_config_path, "rb") as f:
                gateway_config = tomli.load(f)
            gateway_domain_name = gateway_config['host']['domain']
            gateway_port = gateway_config['rathole']['port']
            toml_path = os.path.join(rathole_gateway_path, f"{config['host']['id']}.toml")
            toml_dict = {
                'client': {
                    'remote_addr': f'{gateway_domain_name}:{gateway_port}'
                },
                f"client.services.{config['host']['name']}-jupyter": {
                    'token': 'abc',
                    'local_addr': f"127.0.0.1:{config['jupyter']['port']}"
                }
            }



# # Set ports
# if not config['syncthing']['port']:
#     config['syncthing']['port'] = random.randint(10000, 65536)

# while (not config['jupyter']['port']) or (config['jupyter']['port'] == config['syncthing']['port']):
#     config['jupyter']['port'] = random.randint(10000, 65536)

# while (not config['vnc']['port']) or (config['vnc']['port'] == config['syncthing']['port']) or (config['vnc']['port'] == config['jupyter']['port']):
#     config['vnc']['port'] = random.randint(10000, 65536)

# syncthing_config_path = os.path.join(dir, 'syncthing\config.xml')

# # Initialize the syncthing config file
# syncthing_dir = os.path.join(dir, 'syncthing')
# process = subprocess.Popen(f'syncthing generate --home {syncthing_dir}')
# process.wait()
# tree = ET.parse(syncthing_config_path)
# root = tree.getroot()

# # Get the sycthing id
# host_id = root.find('defaults').find('folder').find('device').attrib['id']
# config['host']['id'] = host_id

# # Clean the devices and folders
# for child in root:
#     if (child.tag == "device") and (child.attrib['id'] != host_id):
#         root.remove(child)
#     elif child.tag == "folder":
#         root.remove(child)

# # Set the sycthing name
# for device in root.findall('device'):
#     if device.attrib['id'] == host_id:
#         if config['host']['name']:
#             device.attrib['name'] = config['host']['name']
#         else:
#             config['host']['name'] = device.attrib['name']
#         break

# # Set the sycthing gui port
# gui_address = root.find('gui').find('address')
# gui_address.text = '127.0.0.1:' + str(config['syncthing']['port'])

# # Add devices
# device_dict = {}
# default_device = root.find('defaults').find('device')
# for device in config['gateways']:
#     device_dict[device['name']] = device['id']
#     new_device = copy.deepcopy(default_device)
#     new_device.attrib['id'] = device['id']
#     new_device.attrib['name'] = device['name']
#     root.append(new_device)

# # Add folders
# default_folder = root.find('defaults').find('folder')
# default_folder_device = root.find('defaults').find('folder').find('device')
# for folder in config['networks']:
#     new_folder = copy.deepcopy(default_folder)
#     new_folder.attrib['id'] = folder['id']
#     new_folder.attrib['label'] = folder['name']
#     new_folder.attrib['path'] = f"networks\\{folder['name']}"
#     for device_name in folder['gateways']:
#         if device_name != config['host']['name']:
#             new_folder_device = copy.deepcopy(default_folder_device)
#             new_folder_device.attrib['id'] = device_dict[device_name]
#             new_folder.append(new_folder_device)
#     root.append(new_folder)

# # Save
# save_config = True
# if save_config:
#     with open(config_path, "wb") as f:
#         tomli_w.dump(config, f)
#     with open(syncthing_config_path, "wb") as f:
#         tree.write(f)

#     networks_path = os.path.join(dir, 'networks')
#     for network in config['networks']:
#         network_path = os.path.join(networks_path, network['name'])
#         if not os.path.exists(network_path):
#             os.makedirs(network_path)
#         remote_configs_path = os.path.join(network_path, 'remote-configs')
#         if not os.path.exists(remote_configs_path):
#             os.makedirs(remote_configs_path)
#         remote_config_path = os.path.join(remote_configs_path, f'{host_id}.toml')
#         shutil.copyfile(config_path, remote_config_path)
