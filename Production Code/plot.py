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

plot = True
tau_cheb_s = []

for i in range(len(q_fits)):
    tau_cheb_s.append([])
    for j in range(len(q_fits[i])):
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

        # Plot the fit just for sanity checks
        if False:
            fig, ax = plt.subplots(2, 2, figsize=(8, 7))

            ax[0,0].plot(data_x, np.mean(fr / data_y[:,np.newaxis] - 1,axis=1))
            ax[0,0].set_xlabel(r'$\log g$')
            ax[0,0].set_ylabel(r'$f_r/f-1$')

            ax[0,1].plot(data_x[qmean > q_min], np.mean(((1/qs)*(fr / data_y[:,np.newaxis] - 1))[qmean > q_min],axis=1))
            ax[0,1].set_xlabel(r'$\log g$')
            ax[0,1].set_ylabel(r'$(1/q)(f_r/f-1)$')

            ax[1,0].plot(data_x, qmean)
            ax[1,0].set_xlabel(r'$\log g$')
            ax[1,0].set_ylabel(r'$q$')

            ax[1,1].plot(data_x[qmean > q_min], np.mean((dt_dlogg * (1/qs)*(fr / data_y[:,np.newaxis] - 1))[qmean > q_min],axis=1))
            ax[1,1].set_xlabel(r'$\log g$')
            ax[1,1].set_ylabel(r'$\tau_{\rm CHeB}$')

            plt.savefig(f'cache/fit_diagnostic_{metal_low:2g}_{metal_high:2g}_{mass_low:2g}_{mass_high:2g}.pdf')
            plt.tight_layout()
            plt.clf()

        # Average tau_cheb over the CHeB
        tau_cheb_s[-1].append((
            metal_low,metal_high,mass_low,mass_high,
            np.mean(np.sum((dlogg * dt_dlogg *(fr / data_y[:,np.newaxis] - 1))[qmean > q_min],axis=0)),
            np.std(np.sum((dlogg * dt_dlogg *(fr / data_y[:,np.newaxis] - 1))[qmean > q_min],axis=0)),
            np.mean(np.sum((dlogg * dt_dlogg *(fr / data_y[:,np.newaxis] - 1))[qmean > q_min],axis=0) / np.sum((dlogg * dt_dlogg)[qmean > q_min],axis=0)),
            np.std(np.sum((dlogg * dt_dlogg *(fr / data_y[:,np.newaxis] - 1))[qmean > q_min],axis=0) / np.sum((dlogg * dt_dlogg)[qmean > q_min],axis=0)),
            N_stars
        ))

tau_cheb_s = np.array(tau_cheb_s)

if plot:

    fig = plt.figure(figsize=(8,5))

    ax = plt.subplot(121)
    masses = 0.5 * (mass_bins[1:] + mass_bins[:-1])
    ax.errorbar(masses, tau_cheb_s[0,:,4]/1e6, yerr=tau_cheb_s[0,:,5]/1e6, label='[M/H]=[-1,-0.5]')
    ax.errorbar(masses, tau_cheb_s[1,:,4]/1e6, yerr=tau_cheb_s[1,:,5]/1e6, label='[M/H]=[-0.5,0.1]')
    ax.errorbar(masses, tau_cheb_s[2,:,4]/1e6, yerr=tau_cheb_s[2,:,5]/1e6, label='[M/H]=[0.1,0.6]')
    ax.axhline(125,linestyle=':', label='MESA V')
    ax.set_xlabel(r'$M_\star/M_\odot$')
    ax.set_ylabel(r'$\tau_{\rm CHeB}/\rm Myr$')
    ax.set_yscale('log')
    ax.legend(loc='lower left', ncol=2)
    ax.set_ylim([3,150])

    ax = plt.subplot(122)
    metals = 0.5 * (mh_bins[1:] + mh_bins[:-1])
    ax.errorbar(metals, tau_cheb_s[:,0,4]/1e6, yerr=tau_cheb_s[:,0,5]/1e6,label=r'$0.9 M_\odot$')
    ax.errorbar(metals, tau_cheb_s[:,1,4]/1e6, yerr=tau_cheb_s[:,1,5]/1e6, label=r'$1.125 M_\odot$')
    ax.errorbar(metals, tau_cheb_s[:,2,4]/1e6, yerr=tau_cheb_s[:,2,5]/1e6, label=r'$1.375 M_\odot$')
    ax.errorbar(metals, tau_cheb_s[:,3,4]/1e6, yerr=tau_cheb_s[:,3,5]/1e6, label=r'$1.625 M_\odot$')
    ax.errorbar(metals, tau_cheb_s[:,4,4]/1e6, yerr=tau_cheb_s[:,4,5]/1e6, label=r'$1.9 M_\odot$')
    ax.axhline(125,linestyle=':', label='MESA V')
    ax.set_xlabel(r'$[M/H]$')
    ax.set_ylabel(r'$\tau_{\rm CHeB}\rm Myr$')
    ax.set_yscale('log')
    ax.legend(loc='lower left', ncol=2)
    ax.set_ylim([3,150])

    plt.savefig('cache/adr.pdf')
    exit()
    # Plot grid
    fig = plt.figure()
    ax = plt.subplot(321)
    cntr = plt.pcolormesh(mass_bins, mh_bins, tau_cheb_s[...,4])
    cbar = fig.colorbar(cntr, ax=ax)
    cbar.ax.set_ylabel(r'$\tau_{\rm CHeB}/\mathrm{yr}$')
    plt.xlabel(r'$M/M_\odot$')
    plt.ylabel(r'$[M/H]$')

    ax = plt.subplot(322)
    cntr = plt.pcolormesh(mass_bins, mh_bins, tau_cheb_s[...,4]/tau_cheb_s[...,5])
    cbar = fig.colorbar(cntr, ax=ax)
    cbar.ax.set_ylabel(r'$\tau_{\rm CHeB}/\sigma_{\tau_{\rm CHeB}}$')
    plt.xlabel(r'$M/M_\odot$')
    plt.ylabel(r'$[M/H]$')

    ax = plt.subplot(323)
    cntr = plt.pcolormesh(mass_bins, mh_bins, tau_cheb_s[...,6])
    cbar = fig.colorbar(cntr, ax=ax)
    cbar.ax.set_ylabel(r'$f_{\rm CHeB} \equiv \tau_{\rm CHeB}/\tau_{\rm RGB}$')
    plt.xlabel(r'$M/M_\odot$')
    plt.ylabel(r'$[M/H]$')

    ax = plt.subplot(324)
    cntr = plt.pcolormesh(mass_bins, mh_bins, tau_cheb_s[...,6]/tau_cheb_s[...,7])
    cbar = fig.colorbar(cntr, ax=ax)
    cbar.ax.set_ylabel(r'$f_{\rm CHeB}/\sigma_{f_{\rm CHeB}}$')
    plt.xlabel(r'$M/M_\odot$')
    plt.ylabel(r'$[M/H]$')

    ax = plt.subplot(325)
    cntr = plt.pcolormesh(mass_bins, mh_bins, tau_cheb_s[...,8])
    cbar = fig.colorbar(cntr, ax=ax)
    cbar.ax.set_ylabel(r'$N_{\rm stars}$')
    plt.xlabel(r'$M/M_\odot$')
    plt.ylabel(r'$[M/H]$')

    plt.tight_layout()
    plt.savefig(f'cache/tau_cheb.pdf')
    plt.clf()
