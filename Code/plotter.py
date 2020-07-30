import numpy as np
import matplotlib.pyplot as plt
from loader import load_history_name


age_index = 2
log_dt_index = 3
log_g_index = 40
log_L_index = 38
log_Teff_index = 37


pms_cutoff = 1e8 # Ignore times before 100 MYr (pre-main sequence)
log_g_RGB_cut = 4.

# Get the 1.2 M_sun Z=0.02 model track
hist = load_history_name('../ModelTracks/m=1.0_z=0.02.data')

# Cut off the pre-main sequence
age = hist[:,age_index]
sel = (age > pms_cutoff)

hist = hist[sel]
age = age[sel]


# Make a quick logTeff cut
log_g = hist[:,log_g_index]
sel = (log_g < log_g_RGB_cut)

log_Teff =  hist[sel, log_Teff_index]
log_g = hist[sel, log_g_index]
dt = 10**hist[sel, log_dt_index] # years
age = np.cumsum(dt) # Starting from when T first fell below RGB_Teff_cut

print(age.shape)
print(log_g.shape)

fig, ax = plt.subplots()
ax.plot(age, log_g)
plt.xlabel('Time Since Start of RGB (years)')
plt.ylabel('$\log g / \mathrm{cm\,s^{-2}}$')
plt.savefig('../Plots/log_g_1.0_msun.pdf')
