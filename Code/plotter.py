import numpy as np
import matplotlib.pyplot as plt
import mesa_reader as mr

pms_cutoff = 1e8 # Ignore times before 100 MYr (pre-main sequence)
log_g_RGB_cut = 3.

# Get the 1.2 M_sun Z=0.02 model track
h=mr.MesaData('../ModelTracks/m=1.0_z=0.02.data')

age = h.star_age

log_g = h.log_g

# Cut off the pre-main sequence and main-sequence
sel = (age > pms_cutoff) & (log_g < log_g_RGB_cut)

log_Teff =  h.log_Teff
dt = 10**h.log_dt
age = np.cumsum(dt[sel]) # Starting from when T first fell below RGB_Teff_cut

print(age.shape)
print(log_g.shape)

fig, ax = plt.subplots()
ax.plot(age, log_g[sel])
plt.xlabel('Time Since Start of RGB (years)')
plt.ylabel('$\log g / \mathrm{cm\,s^{-2}}$')
plt.savefig('../Plots/log_g_1.0_msun.pdf')
