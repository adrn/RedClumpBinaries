import mesa_reader as mr
import numpy as np
from pickle import dump

pms_cutoff = 1e8 # Ignore times before 100 MYr (pre-main sequence)
log_g_RGB_cut = 3.

metallicities = [(0.005,'main_Z_sweep_time_2022_02_07_10_57_16_sha_0b9f'),
				(0.01,'main_Z_sweep_time_2022_02_07_10_57_22_sha_bdd5'),
				(0.015,'main_Z_sweep_time_2022_02_07_10_57_27_sha_b219')
				]

masses = [1.0,1.2,1.4,1.6,1.8,2.0]


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

data = {(m,z):process_hist(hs[(m,z)]) for m,z in hs.keys()}

dump([masses,metallicities,data],open('cache/mesa_parsed.data','wb'))
