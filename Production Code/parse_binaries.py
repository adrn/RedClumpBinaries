# Imports
import pathlib

import astropy.table as at
import astropy.units as u
import h5py
import numpy as np

import arviz as az
from aesara_theano_fallback import tensor as tt
import pymc3 as pm
import pymc3_ext as pmx

from apogee_helpers import download_file
from pickle import dump

# Caching
local_cache_path = pathlib.Path('../data/').resolve().absolute()
local_cache_path.mkdir(exist_ok=True)

# Get APOGEE data
allstar_path = local_cache_path / 'allStarLite-dr17-synspec_rev1.fits'
if not allstar_path.exists():
    url = "https://data.sdss.org/sas/dr17/apogee/spectro/aspcap/dr17/synspec_rev1/allStarLite-dr17-synspec_rev1.fits"
    download_file(
        url, 
        local_path=allstar_path.parent, 
        local_filename=allstar_path.parts[-1]
    )
allstar = at.QTable.read(allstar_path)

# Get metadata
metadata_path = local_cache_path / 'metadata.fits'
if not metadata_path.exists():
    url = "https://users.flatironinstitute.org/~apricewhelan/data/apogee-dr17-binaries/metadata.fits"
    download_file(
        url, 
        local_path=metadata_path.parent, 
        local_filename=metadata_path.parts[-1]
    )
metadata = at.QTable.read(metadata_path)
metadata = at.unique(at.join(allstar, metadata, keys='APOGEE_ID'), 
                     keys='APOGEE_ID')

# Find binaries
llr_const = metadata['max_unmarginalized_ln_likelihood'] - metadata['robust_constant_ln_likelihood']
binaries_mask = (llr_const > 4)

# Write in a faster-loading format.
metadata = {'LOGG': metadata['LOGG'], 'M_H': metadata['M_H']}

dump([metadata, binaries_mask],open('cache/parsed.data','wb'))
