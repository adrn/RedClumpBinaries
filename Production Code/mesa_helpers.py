import mesa_reader as mr
import numpy as np

pms_cutoff = 1e8 # Ignore times before 100 MYr (pre-main sequence)
log_g_RGB_cut = 3.

# Get the 1.2 M_sun Z=0.02 model track
h=mr.MesaData('../ModelTracks/m=1.0_z=0.02.data')

age = h.star_age
log_g_MESA = h.log_g
dt = 10**h.log_dt

# Cut off the pre-main sequence and main-sequence
sel = (age > pms_cutoff) & (log_g_MESA < log_g_RGB_cut)

dt = dt[sel]
age = np.cumsum(dt) # Age from the start of the RGB
log_g_MESA = log_g_MESA[sel]

# Find the TRGB
i_TRGB = np.argmin(log_g_MESA)

def dt_dlogg_ascent(log_g, dlog_g):
	ran = np.where(
			(log_g_MESA > log_g - dlog_g/2) &
			(log_g_MESA < log_g + dlog_g/2) &
			(age < age[i_TRGB])
		)

	dage = np.sum(age[ran])

	return dage/dlog_g

