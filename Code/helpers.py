import pathlib
from urllib.request import urlopen
import requests
from tqdm import tqdm
import astropy.table as at


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


local_cache_path = pathlib.Path('../data/').resolve().absolute()
local_cache_path.mkdir(exist_ok=True)


def get_allstar():
    allstar_path = local_cache_path / 'allStarLite-dr17-synspec_rev1.fits'
    if not allstar_path.exists():
        url = "https://data.sdss.org/sas/dr17/apogee/spectro/aspcap/dr17/synspec_rev1/allStarLite-dr17-synspec_rev1.fits"
        download_file(
            url, 
            local_path=allstar_path.parent, 
            local_filename=allstar_path.parts[-1]
        )
    allstar = at.QTable.read(allstar_path)
    return allstar


def get_metadata():
    metadata_path = local_cache_path / 'metadata.fits'
    if not metadata_path.exists():
        url = "https://users.flatironinstitute.org/~apricewhelan/data/apogee-dr17-binaries/metadata.fits"
        download_file(
            url, 
            local_path=metadata_path.parent, 
            local_filename=metadata_path.parts[-1]
        )
    metadata = at.QTable.read(metadata_path)
    return metadata


