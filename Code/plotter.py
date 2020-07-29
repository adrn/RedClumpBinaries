import numpy as np
import matplotlib.pyplot as plt
from loader import load_history_name


age_index = 2
dt_index = 3
log_g_index = 40
log_L_index = 38
log_Teff_index = 37

pms_cutoff = 1e8 # Ignore times before 100 MYr
agb_cutoff = 6.4e9

# Get the 1.2 M_sun Z=0.02 model track
hist = load_history_name('../ModelTracks/m=1.2_z=0.02.data')

# Extract log_g and log_Teff, slice by age
age = hist[:,age_index]
sel = (age > pms_cutoff) & (age < agb_cutoff)
log_g = hist[sel, log_g_index]
log_Teff = hist[sel, log_Teff_index]
log_L = hist[sel, log_L_index]
age = age[sel]

fig, ax = plt.subplots()

ax.plot(10**log_Teff, log_L)
ax.set_xlim([5000,3000])
ax.set_ylim([1,3.5])
plt.show()
