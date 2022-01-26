import pathlib
from urllib.request import urlopen
import requests
from tqdm import tqdm


def download_file(url, local_path=None, local_filename=None, block_size=102400):
    if local_path is None:
        local_path = '.'
    local_path = pathlib.Path(local_path).resolve().absolute()
    if local_filename is None:
        local_filename = url.split('/')[(-1)]
    full_local_path = local_path / local_filename
    site = urlopen(url)
    meta = site.info()
    total_size = int(meta['Content-Length'])
    response = requests.get(url, stream=True)
    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
    with open(full_local_path, 'wb') as f:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)

    progress_bar.close()
    return full_local_path
