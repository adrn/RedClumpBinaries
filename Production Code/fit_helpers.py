from scipy.stats import norm
import numpy as np
from aesara_theano_fallback import tensor as tt
import pymc3 as pm
import pymc3_ext as pmx
from config import logg_lims

def q(x,mu,sigma):
    return norm.pdf((x-mu)/sigma)

def line(x, slope, const_y):
    y = slope * x + const_y
    return y

def fit_line(x, y, yerr):
    init_const = np.nanmedian(y)
    init_slope = 0.5

    with pm.Model() as model:    
        const_y = pm.Uniform('const_y', 0., 1)
        slope = pm.Uniform('slope', 1e-4, 1)

        model_y = slope * x + const_y
        lnlike = pm.Normal('lnlike', mu=model_y, sd=yerr, observed=y)

        res = pmx.optimize(start={
            'const_y': init_const,
            'slope': init_slope
        })

        samples = pmx.sample(start=res, return_inferencedata=True, cores=4)
    
    return res, samples

def fit_mixture_model(logg_data):
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
    
    return res, grid, prob_density