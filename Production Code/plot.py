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
q_fits = load(open('cache/q_fits.data','rb'))
fr_fits = load(open('cache/fr_fits.data','rb'))

for i in range(len(q_fits)):
    # Unpack fit data
    m_min, m_max, metal_mask, q_res, _, _ = q_fits[i]
    _, _, _, slope, offset = fr_fits[i]

    # Bin binary fraction in log(g)
    data_x, data_y, data_yerr = bin_f_binary_in_logg(metadata, binaries_mask, metal_mask, logg_bins)

    # Calculate fr and q
    fr = data_x * slope + offset
    qs = q(data_x, q_res['mu_logg'], np.exp(q_res['logsigma_logg']))

    # Plot the fit just for sanity checks
    fig, ax = plt.subplots(2, 2, figsize=(6, 5))

    ax[0,0].plot(data_x, fr / data_y - 1)
    ax[0,0].set_xlabel(r'$\log g$')
    ax[0,0].set_ylabel(r'$f_r/f-1$')

    ax[0,1].plot(data_x, (1/qs)*(fr / data_y - 1))
    ax[0,1].set_xlabel(r'$\log g$')
    ax[0,1].set_ylabel(r'$(1/q)(f_r/f-1)$')

    ax[1,0].plot(data_x, qs)
    ax[1,0].set_xlabel(r'$\log g$')
    ax[1,0].set_ylabel(r'$q$')

    plt.savefig(f'cache/fit_diagnostic_{m_min:2g}_{m_max:2g}.pdf')
    plt.clf()
