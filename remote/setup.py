import os
import requests
import zipfile

def download(url: str, dest_folder: str, filename=None):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    if filename is None:
        filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
    file_path = os.path.join(dest_folder, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))

dir = os.path.dirname(os.path.realpath(__file__))
url = 'https://github.com/rapiz1/rathole/releases/download/v0.4.7/rathole-x86_64-pc-windows-msvc.zip'
download(url, dir, 'rathole.zip')
rathole_path = os.path.join(dir, 'rathole.zip')
rathole_dir = os.path.join(dir, 'rathole')
with zipfile.ZipFile(rathole_path, 'r') as zip_ref:
    zip_ref.extractall(rathole_dir)
os.remove(rathole_path)
