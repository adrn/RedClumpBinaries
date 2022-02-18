import numpy as np
from pickle import load

masses,metallicities,data = load(open('cache/mesa_parsed.data','rb'))

def get_dt_dlogg_ascent_single(mass, metallicity, log_g, dlog_g):
	log_g_MESA, age, i_TRGB, dt = data[(round(mass,5),round(metallicity,5))]

	ran = np.where(
			(log_g_MESA > log_g - dlog_g/2) &
			(log_g_MESA < log_g + dlog_g/2) &
			(age < age[i_TRGB])
		)

	dage = np.sum(dt[ran])

	return dage/dlog_g


def dt_dlogg_ascent(mass, metallicity, log_g, dlog_g):
	for i in range(len(metallicities)):
		if metallicities[i][0] <= metallicity:
			if abs(metallicities[i][0] - metallicity) < 1e-3:
				return get_dt_dlogg_ascent_single(mass, metallicity[i][0], log_g, dlog_g)
			elif metallicity <= metallicities[i+1][0]:
				metal_low = metallicities[i][0]
				metal_high = metallicities[i+1][0]

				low = get_dt_dlogg_ascent_single(mass, metal_low, log_g, dlog_g)
				high = get_dt_dlogg_ascent_single(mass, metal_high, log_g, dlog_g)

				return (low * (metallicity - metal_low) + high * (metal_high - metallicity)) / (metal_high - metal_low)
