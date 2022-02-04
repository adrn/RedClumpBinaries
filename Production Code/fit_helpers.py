from scipy.stats import norm
import numpy as np
from aesara_theano_fallback import tensor as tt
import pymc3 as pm
import pymc3_ext as pmx

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

        samples = pmx.sample(start=res, return_inferencedata=True, cores=1)
    
    return res, samples
