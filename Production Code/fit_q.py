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

from config import mh_bins, logg_lims, mass_bins
from slice_helpers import mask_metallicity_and_mass
from fit_helpers import fit_mixture_model
from pickle import load, dump

metadata, binaries_mask = load(open('cache/parsed.data','rb'))

# Loop over metallicity and mass bins and fit a Gaussian+background model.
opts = []
for metal_low, metal_high in list(zip(mh_bins[:-1], mh_bins[1:])) + [(mh_bins.min(), mh_bins.max())]:
    opts.append([])
    for mass_low, mass_high in list(zip(mass_bins[:-1], mass_bins[1:])) + [(mass_bins.min(), mass_bins.max())]:
        print('Fitting metallicity range',metal_low,metal_high,'and mass range',mass_low,mass_high)

        mask = mask_metallicity_and_mass(metadata, metal_low, metal_high, mass_low, mass_high)
        logg_data = metadata['LOGG'][mask]
        
        res, grid, prob_density, samples = fit_mixture_model(logg_data)
        opts[-1].append([metal_low,metal_high,mass_low,mass_high,mask,res,logg_data,prob_density,samples])

        # Plot the fit just for sanity checks
        plt.figure()
        plt.hist(logg_data, 
                 bins=50, density=True, histtype='step')
        plt.plot(grid, prob_density)
        plt.xlabel(r'$\log g$')
        plt.ylabel(r'$dN_\star/d\log g$')
        plt.savefig(f'cache/q_fit_{metal_low:2g}_{metal_high:2g}_{mass_low:2g}_{mass_high:2g}.pdf')
        plt.clf()

dump(opts,open('cache/q_fits.data','wb'))
