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

from pickle import load, dump

metadata, binaries_mask = load(open('cache/parsed.data','rb'))

# Loop over metallicity bins and fit a Gaussian+background model.
opts = []
for l, r in list(zip(mh_bins[:-1], mh_bins[1:])) + [(mh_bins.min(), mh_bins.max())]:
    print('Fitting metallicity range',l,r)
    mask = mask_metallicity(metadata,l,r)
    logg_data = metadata['LOGG'][mask]
    
    with pm.Model() as model:
        # Gaussian distribution with mean uniform on [2,3]
        # and sigma log-uniform distributed on [1e-4,1e1]
        mu = pm.Uniform('mu_logg', 2, 3)
        logsigma = pm.Uniform('logsigma_logg', -4, 1)
        sigma = tt.exp(logsigma)
        dist1 = pm.Normal.dist(mu, sigma)

        # Gaussian distribution with mean uniform on [-5,5]
        # and sigma log-uniform distributed on [1,1e4].
        # This sigma distribution ensures that this part of the fit
        # is for a very broad distribution, which serves as our background.
        mu_bg = pm.Uniform('mu_bg', -5, 5)
        logsigma_bg = pm.Uniform('logsigma_bg', 0, 4)
        sigma_bg = tt.exp(logsigma_bg)
        dist2 = pm.TruncatedNormal.dist(mu_bg, sigma_bg, 
                                        lower=logg_lims[0], upper=logg_lims[1])

        # Construct the mixture model
        w = pm.Dirichlet('w', a=np.array([1, 1]))
        lnlike = pm.Mixture('lnlike', w=w, comp_dists=[dist1, dist2], 
                            observed=logg_data)

        # Put on a fine grid in log(g)
        grid = np.linspace(*logg_lims, 1024)
        lnlike_grid1 = dist1.logp(grid) + tt.log(w[0])
        lnlike_grid2 = dist2.logp(grid) + tt.log(w[1])
        lnlike_grid = pm.logaddexp(lnlike_grid1, lnlike_grid2)
        
    with model:
        # Fit the model
        res = pmx.optimize(start={
            'mu_logg': 2.4, 'logsigma_logg': -2.3, 'mu_bg': 1, 'logsigma_bg': 2})
        
        # Store the distribution in case we want to plot it
        prob_density = np.exp(pmx.eval_in_model(lnlike_grid, point=res))
    
    opts.append([l,r,mask,res,logg_data,prob_density])

    # Plot the fit just for sanity checks
    plt.figure()
    plt.hist(logg_data, 
             bins=50, density=True, histtype='step')
    plt.plot(grid, prob_density)
    plt.xlabel(r'$\log g$')
    plt.ylabel('Number Density of Stars')
    plt.savefig(f'cache/q_fit_{l:2g}_{r:2g}.pdf')
    plt.clf()

dump(opts,open('cache/q_fits.data','wb'))
