import numpy as np
from pickle import load

masses,metallicities,data = load(open('cache/mesa_parsed.data','rb'))

def get_dt_dlogg_ascent_single(mass, metallicity, log_g, dlog_g):
	log_g_MESA, age, i_TRGB, dt = data[(mass,metallicity[0])]

	ran = np.where(
			(log_g_MESA > log_g - dlog_g/2) &
			(log_g_MESA < log_g + dlog_g/2) &
			(age < age[i_TRGB])
		)

	dage = np.sum(dt[ran])

	return dage/dlog_g

def dt_dlogg_ascent(mass, metallicity, log_g, dlog_g):

	i_mass = -1
	for i in range(len(masses)-1):
		if masses[i] <= mass and masses[i+1] >= mass:
			mix_i0 = (mass - masses[i])/(masses[i+1]-masses[i])
			mix_i1 = 1 - mix_i0
			i_mass = i
	if i_mass == -1:
		print('Error: out of bounds mass',mass)
		i_mass = 0
		mix_i0 = 1
		mix_i1 = 0
#		exit()

	i_metal = -1
	for i in range(len(metallicities)-1):
		if metallicities[i][0] <= metallicity and metallicities[i+1][0] >= metallicity:
			mix_j0 = (metallicity - metallicity[i][0])/(metallicity[i+1][0]-metallicity[i][0])
			mix_j1 = 1 - mix_i0
			i_metal = i
	if i_metal == -1:
		print('Error: out of bounds metal',metallicity)
		i_metal = 0
		mix_j0 = 1
		mix_j1 = 0
#		exit()


	d_00 = get_dt_dlogg_ascent_single(masses[i_mass],   metallicities[i_metal],    log_g, dlog_g)
	d_01 = get_dt_dlogg_ascent_single(masses[i_mass],   metallicities[i_metal+1],  log_g, dlog_g)
	d_10 = get_dt_dlogg_ascent_single(masses[i_mass+1], metallicities[i_metal],    log_g, dlog_g)
	d_11 = get_dt_dlogg_ascent_single(masses[i_mass+1], metallicities[i_metal+1],  log_g, dlog_g)

	d_0 = d_00 * mix_j0 + d_01 * mix_j1
	d_1 = d_10 * mix_j0 + d_11 * mix_j1

	return d_0 * mix_i0 + d_1 * mix_i1
