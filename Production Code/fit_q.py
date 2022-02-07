import astropy.table as at
import astropy.units as u
import h5py
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import arviz as az
from aesara_theano_fallback import tensor as tt
import pymc3 as pm
import pymc3_ext as pmx

from config import mh_bins, logg_lims
from slice_helpers import mask_metallicity
from fit_helpers import fit_mixture_model
from pickle import load, dump

metadata, binaries_mask = load(open('cache/parsed.data','rb'))

# Loop over metallicity and mass bins and fit a Gaussian+background model.
opts = []
for l, r in list(zip(mh_bins[:-1], mh_bins[1:])) + [(mh_bins.min(), mh_bins.max())]:
    print('Fitting metallicity range',l,r)
    mask = mask_metallicity(metadata,l,r)
    logg_data = metadata['LOGG'][mask]
    
    res, prob_density = fit_mixture_model(logg_data)
    opts.append([l,r,mask,res,logg_data,prob_density])

    # Plot the fit just for sanity checks
    plt.figure()
    plt.hist(logg_data, 
             bins=50, density=True, histtype='step')
    plt.plot(grid, prob_density)
    plt.xlabel(r'$\log g$')
    plt.ylabel(r'$dN_\star/d\log g$')
    plt.savefig(f'cache/q_fit_{l:2g}_{r:2g}.pdf')
    plt.clf()

dump(opts,open('cache/q_fits.data','wb'))
