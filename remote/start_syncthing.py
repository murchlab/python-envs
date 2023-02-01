import os
import subprocess

dir = os.path.dirname(os.path.realpath(__file__))
# os.chdir(dir)
syncthing_dir = os.path.join(dir, 'syncthing')
subprocess.Popen(f'syncthing --home {syncthing_dir}')
