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

from config import logg_lims, logg_bins, q_min, dlogg, mass_bins, mh_bins, Z_solar
from slice_helpers import bin_f_binary_in_logg
from fit_helpers import q, fit_line
from pickle import load, dump
from mesa_helpers import dt_dlogg_ascent

metadata, binaries_mask = load(open('cache/parsed.data','rb'))
q_fits = load(open('cache/q_fits.data','rb'))
fr_fits = load(open('cache/fr_fits.data','rb'))

tau_cheb_s = []

for j in range(len(q_fits[0])):
    for i in range(len(q_fits)):
        # Load fr samples
        metal_low,metal_high,mass_low,mass_high,metal_mass_mask,slope,offset,fr_samples = fr_fits[i][j]

        # Bin binary fraction in log(g)
        data_x, data_y, data_yerr, H_all = bin_f_binary_in_logg(metadata, binaries_mask, metal_mass_mask, logg_bins)

        # Calculate fr
        slope = fr_samples.posterior.slope.values.flatten()
        offset = fr_samples.posterior.const_y.values.flatten()
        fr = data_x[:,np.newaxis] * slope[np.newaxis,:] + offset[np.newaxis,:]

        # Calculate q
        _,_,_,_,_, qres, _, _, q_samples = q_fits[i][j]
        qmean = q(data_x, qres['mu_logg'], np.exp(qres['logsigma_logg']))
        mu = q_samples.posterior.mu_logg.values.flatten()
        sigma = np.exp(q_samples.posterior.logsigma_logg.values.flatten())
        qs = q(data_x[:,np.newaxis], mu[np.newaxis,:], sigma[np.newaxis,:])

        # Number of stars
        N_stars = int(sum(H_all[qmean > q_min]))

        # Get dt/dlog(g) for the ascent
        mass = 0.5 * (mass_low + mass_high)
        metal = Z_solar * 10**(0.5 * (metal_low + metal_high))
        dt_dlogg = np.array(list(dt_dlogg_ascent(mass, metal, logg, dlogg) for logg in data_x))[:,np.newaxis]

        logg_start, logg_end = min(data_x[qmean > q_min]),max(data_x[qmean > q_min])

        # Average tau_cheb over the CHeB
        tau_cheb_s.append((
            metal_low,metal_high,mass_low,mass_high,logg_start,logg_end,N_stars,
            np.mean(np.sum((dlogg * dt_dlogg *(fr / data_y[:,np.newaxis] - 1))[qmean > q_min],axis=0)),
            np.std(np.sum((dlogg * dt_dlogg *(fr / data_y[:,np.newaxis] - 1))[qmean > q_min],axis=0)),
            np.sum((dlogg * dt_dlogg)[qmean > q_min]),
            np.mean(np.mean(((fr / data_y[:,np.newaxis] - 1))[qmean > q_min],axis=0)),
            np.std(np.mean(((fr / data_y[:,np.newaxis] - 1))[qmean > q_min],axis=0)),
        ))

tau_cheb_s = np.array(tau_cheb_s)
print(tau_cheb_s)

s = ''
s = s + r'\tablehead{'
s = s + r'\colhead{$(M_\star/M_\odot)_{\rm min}$} &'
s = s + r'\colhead{$(M_\star/M_\odot)_{\rm max}$} &'
s = s + r'\colhead{$[\mathrm{M}/\mathrm{H}]_{\rm min}$} &'
s = s + r'\colhead{$[\mathrm{M}/\mathrm{H}]_{\rm max}$} &'
s = s + r'\colhead{$N_{\rm stars}$} &'
s = s + r'\colhead{$\log g_{\rm min}$} &'
s = s + r'\colhead{$\log g_{\rm max}$} &'
s = s + r'\colhead{$\tau_{\rm RGB}/\mathrm{Myr}$} &'
s = s + r'\colhead{$\tau_{\rm CHeB}/\mathrm{Myr}$} &'
s = s + r'\colhead{$\sigma_{\tau_{\rm CHeB}}/\mathrm{Myr}$} &'
s = s + r'\colhead{$f_{\rm CHeB}$} &'                           # Binary deficit
s = s + r'\colhead{$\sigma_{f_{\rm CHeB}}$}'
s = s + '}\n\startdata\n'
for metal_min, metal_max, mass_min, mass_max, logg_start, logg_end, N_stars, tau, tau_sigma, tau_RGB, f, f_sigma in tau_cheb_s:
    s = s + f'{mass_min:.2g} & {mass_max:2g} & {metal_min:.2g} & {metal_max:.2g} & {int(N_stars)} & {logg_start:2g}& {logg_end:2g} & {tau_RGB/1e6:.2g} & {tau/1e6:.2g} & {tau_sigma/1e6:.2g} & {f:.2g} & {f_sigma:.2g} \\\\\n'
s = s + '\enddata\n'

fi = open('../writeup/table.tex','w+')
fi.write(s)
fi.close()
