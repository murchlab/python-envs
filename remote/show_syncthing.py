import os
import tomli
import webbrowser

dir = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(dir, 'configs\config.toml')
with open(config_path, "rb") as f:
        config = tomli.load(f)

port =  config['syncthing']['port']

url = f'http://localhost:{port}'
webbrowser.open(url, new=0, autoraise=True)
