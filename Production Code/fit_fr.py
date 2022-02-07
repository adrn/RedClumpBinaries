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

from config import logg_lims, logg_bins, q_min
from slice_helpers import bin_f_binary_in_logg
from fit_helpers import q, fit_line
from pickle import load, dump

metadata, binaries_mask = load(open('cache/parsed.data','rb'))
opts = load(open('cache/q_fits.data','rb'))

fr_fits = []
for metal_low,metal_high,mass_low,mass_high,metal_mass_mask,q_res,_,_ in opts:
    # Bin binary fraction in log(g)
    data_x, data_y, data_yerr = bin_f_binary_in_logg(metadata, binaries_mask, metal_mass_mask, logg_bins)

    # Exclude the Red Clump from the fit
    qs = q(logg_bins, q_res['mu_logg'], np.exp(q_res['logsigma_logg']))
    exclusion = (min(logg_bins[qs > q_min]),max(logg_bins[qs > q_min]))

    print('CHeB is in log(g)=',exclusion)

    fit_idx = (
        (data_x > logg_lims[0]) &
        np.logical_not((data_x > exclusion[0]) & (data_x < exclusion[1])) &
        (data_x < logg_lims[1])
    )

    fit_x = data_x[fit_idx]
    fit_y = data_y[fit_idx]
    fit_yerr = data_yerr[fit_idx]

    # Fit a line 
    res, samples = fit_line(fit_x, fit_y, fit_yerr)

    slope = res['slope']
    offset = res['const_y']

    fr_fits.append((metal_low,metal_high,mass_low,mass_high,metal_mass_mask,slope,offset))

    # Plot the fit just for sanity checks
    fig, ax = plt.subplots(1, 1, figsize=(6, 5))

    ax.plot(data_x,
            data_x * slope + offset,
            marker='', zorder=10)

    ax.errorbar(data_x,
                data_y,
                data_yerr,
                ecolor='#aaaaaa', ls='none', marker='', zorder=5)

    ax.set_xlabel(r'$\log g$')
    ax.set_ylabel('Binary Fraction')
    plt.savefig(f'cache/fr_fit_{metal_low:2g}_{metal_high:2g}_{mass_low:2g}_{mass_high:2g}.pdf')
    plt.clf()

dump(fr_fits,open('cache/fr_fits.data','wb'))
