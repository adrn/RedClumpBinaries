import mesa_reader as mr
import numpy as np
from pickle import dump
from config import Z_solar

pms_cutoff = 1e8 # Ignore times before 100 MYr (pre-main sequence)
log_g_RGB_cut = 3.

metallicities = [
				(Z_solar*10**-1,'main_Z_sweep_time_2022_02_14_10_07_29_sha_a803'),
				(Z_solar*10**-0.6,'main_Z_sweep_time_2022_02_14_10_07_34_sha_2595'),
				(Z_solar*10**-0.2,'main_Z_sweep_time_2022_02_14_10_07_40_sha_8110'),
				(Z_solar*10**0.2,'main_Z_sweep_time_2022_02_14_10_07_46_sha_96cd'),
				(Z_solar*10**0.6,'main_Z_sweep_time_2022_02_14_10_07_51_sha_2bd0')
				]

masses = [0.9,1.125,1.375,1.625,1.875]


data_dir = '/Users/ajermyn/Dropbox/Active_Projects/RedClumpBinaries/MESA_models/runs/'

# Get the model tracks
hs = {}
for m in masses:
	for z,zdir in metallicities:
		print('Reading model with M=',m,'Z=',z)
		hs[(m,z)] = mr.MesaData(data_dir + f'{zdir}/runs/{m}/LOGS/history.data')

def process_hist(h):
	age = h.star_age
	log_g_MESA = h.log_g
	dt = 10**h.log_dt

	# Cut off the pre-main sequence and main-sequence
	sel = (age > pms_cutoff) & (log_g_MESA < log_g_RGB_cut)

	log_g_MESA = log_g_MESA[sel]
	dt = dt[sel]
	age = np.cumsum(dt) # Age from the start of the RGB

	# Find the TRGB
	i_TRGB = np.argmin(log_g_MESA)

	return log_g_MESA, age, i_TRGB, dt

data = {(round(m,5),round(z,5)):process_hist(hs[(m,z)]) for m,z in hs.keys()}

dump([masses,metallicities,data],open('cache/mesa_parsed.data','wb'))
