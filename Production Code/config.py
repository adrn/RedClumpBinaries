import numpy as np

logg_lims = (1.8, 3.2)
dlogg = 0.05
logg_bins = np.arange(*logg_lims, dlogg)

n_metal_bins = 3
metallicity_lims = (-1, 0.6) # log[M/H]
mh_bins = np.linspace(*metallicity_lims, n_metal_bins + 1)

q_min = 0.1 # Defines the edge of the CHeB.
			# Smaller values include more of the CHeB but increase sensitivity to fits/noise.

mass_lims = (0.8,2.5)
mass_bins = np.array([0.8,1,1.25,1.5,2,2.5])