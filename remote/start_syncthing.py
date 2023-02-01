import os
import subprocess

dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir)
syncthing_dir = os.path.join(dir, 'syncthing')

# With output
# subprocess.Popen(f'syncthing --no-browser --home {syncthing_dir}')

# Without output
subprocess.Popen(f'syncthing --no-browser --home {syncthing_dir}', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
