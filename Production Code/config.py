import numpy as np

logg_lims = (1.8, 3.2)
logg_bins = np.arange(*logg_lims, 0.05)

n_metal_bins = 4
metallicity_lims = (-1.5, 0.6) # log[M/H]
mh_bins = np.linspace(*metallicity_lims, n_metal_bins + 1)

q_min = 0.05 # Defines the edge of the CHeB.
			 # Smaller values include more of the CHeB but increase sensitivity to fits/noise.