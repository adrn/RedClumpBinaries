import numpy as np

logg_lims = (1.8, 3.2)
dlogg = 0.05
logg_bins = np.arange(*logg_lims, dlogg)

n_metal_bins = 3
Z_solar = 0.014
metallicity_lims = (-1, 0.6) # log[M/H]
mh_bins = np.linspace(*metallicity_lims, n_metal_bins + 1)

q_min = 0.1 # Defines the edge of the CHeB.
			# Smaller values include more of the CHeB but increase sensitivity to fits/noise.

mass_bins = np.array([0.8,1,1.25,1.5,1.75,2]) # We chop the upper mass range because we don't want the secondary clump.
mass_lims = (mass_bins.min(), mass_bins.max())
