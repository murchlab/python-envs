import os
import tomli
import subprocess

dir = os.path.dirname(os.path.realpath(__file__))
rathole_path = os.path.join(dir, 'rathole\\rathole.exe')
config_path = os.path.join(dir, 'configs\config.toml')
with open(config_path, "rb") as f:
    config = tomli.load(f)
os.chdir(dir)

# With output
# subprocess.Popen(f'syncthing --no-browser --home {syncthing_dir}')

# Without output
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
        gateway_config_path = os.path.join(network_path, f'remote-configs\{gateway}.toml')
        with open(gateway_config_path, "rb") as f:
            gateway_config = tomli.load(f)
        gateway_domain_name = gateway_config['host']['domain-name']
        gateway_port = gateway_config['rathole']['port']

        toml_path = os.path.join(rathole_gateway_path, f"{config['host']['name']}.toml")
        subprocess.Popen(f'{rathole_path} {toml_path}')
        # subprocess.Popen(f'{rathole_path} {toml_path}', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
