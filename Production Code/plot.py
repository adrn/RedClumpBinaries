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

plot = False
tau_cheb_s = []

for i in range(len(q_fits)):
    tau_cheb_s.append([])
    for j in range(len(q_fits[i])):
        # Load fr samples
        metal_low,metal_high,mass_low,mass_high,metal_mass_mask,slope,offset,fr_samples = fr_fits[i][j]

        # Bin binary fraction in log(g)
        data_x, data_y, data_yerr = bin_f_binary_in_logg(metadata, binaries_mask, metal_mass_mask, logg_bins)

        # Calculate fr
        slope = fr_samples.posterior.slope.values.flatten()
        offset = fr_samples.posterior.const_y.values.flatten()
        fr = data_x[:,np.newaxis] * slope[np.newaxis,:] + offset[np.newaxis,:]

        # Calculate q
        _,_,_,_,_, _, _, _, q_samples = q_fits[i][j]
        mu = q_samples.posterior.mu_logg.values.flatten()
        sigma = np.exp(q_samples.posterior.logsigma_logg.values.flatten())
        qs = q(data_x[:,np.newaxis], mu[np.newaxis,:], sigma[np.newaxis,:])


        # Get dt/dlog(g) for the ascent
        mass = 0.5 * (mass_low + mass_high)
        metal = Z_solar * 10**(0.5 * (metal_low + metal_high))
        dt_dlogg = np.array(list(dt_dlogg_ascent(mass, metal, logg, dlogg) for logg in data_x))[:,np.newaxis]

        # Plot the fit just for sanity checks
        if plot:
            fig, ax = plt.subplots(2, 2, figsize=(8, 7))

            ax[0,0].plot(data_x, np.mean(fr / data_y[:,np.newaxis] - 1,axis=1))
            ax[0,0].set_xlabel(r'$\log g$')
            ax[0,0].set_ylabel(r'$f_r/f-1$')

            ax[0,1].plot(data_x[qs > q_min], np.mean(((1/qs)*(fr / data_y[:,np.newaxis] - 1))[qs > q_min],axis=1))
            ax[0,1].set_xlabel(r'$\log g$')
            ax[0,1].set_ylabel(r'$(1/q)(f_r/f-1)$')

            ax[1,0].plot(data_x, qs)
            ax[1,0].set_xlabel(r'$\log g$')
            ax[1,0].set_ylabel(r'$q$')

            ax[1,1].plot(data_x[qs > q_min], np.mean((dt_dlogg * (1/qs)*(fr / data_y[:,np.newaxis] - 1))[qs > q_min],axis=1))
            ax[1,1].set_xlabel(r'$\log g$')
            ax[1,1].set_ylabel(r'$\tau_{\rm CHeB}$')

            plt.savefig(f'cache/fit_diagnostic_{metal_low:2g}_{metal_high:2g}_{mass_low:2g}_{mass_high:2g}.pdf')
            plt.tight_layout()
            plt.clf()

        # Average tau_cheb over the CHeB
        tau_cheb_s[-1].append((
            metal_low,metal_high,mass_low,mass_high,
            np.mean(np.sum((dlogg * dt_dlogg *(fr / data_y[:,np.newaxis] - 1))[qs > q_min],axis=0)),
            np.std(np.sum((dlogg * dt_dlogg *(fr / data_y[:,np.newaxis] - 1))[qs > q_min],axis=0)),
            np.mean(np.sum((dlogg * dt_dlogg *(fr / data_y[:,np.newaxis] - 1))[qs > q_min],axis=0) / np.sum((dlogg * dt_dlogg)[qs > q_min],axis=0)),
            np.std(np.sum((dlogg * dt_dlogg *(fr / data_y[:,np.newaxis] - 1))[qs > q_min],axis=0) / np.sum((dlogg * dt_dlogg)[qs > q_min],axis=0))
        ))


tau_cheb_s = np.array(tau_cheb_s)

print(tau_cheb_s)

if plot:
    # Plot grid
    fig = plt.figure()
    ax = plt.subplot(111)
    cntr = plt.pcolormesh(mass_bins, mh_bins, tau_cheb_s[:-1,:-1,4])
    cbar = fig.colorbar(cntr, ax=ax)
    cbar.ax.set_ylabel(r'$\tau_{\rm CHeB}/\mathrm{yr}$')
    plt.xlabel(r'$M/M_\odot$')
    plt.ylabel(r'$[M/H]$')
    plt.savefig(f'cache/tau_cheb.pdf')
    plt.clf()

    fig = plt.figure()
    ax = plt.subplot(111)
    cntr = plt.pcolormesh(mass_bins, mh_bins, tau_cheb_s[:-1,:-1,5], vmin=0.5, vmax=3)
    cbar = fig.colorbar(cntr, ax=ax)
    cbar.ax.set_ylabel(r'$\tau_{\rm CHeB}/\tau_{\rm RGB}$')
    plt.xlabel(r'$M/M_\odot$')
    plt.ylabel(r'$[M/H]$')
    plt.savefig(f'cache/tau_cheb_div_tau_RGB.pdf')
    plt.clf()
