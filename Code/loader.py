import numpy as np

def load_prof_index():
	rows = []
	counter = 0
	for row in open('LOGS/profiles.index'):
		if counter > 0:
			data = row.split(' ')
			data = list(d for d in data if len(d) > 0)
			data = list(float(d) for d in data)
			rows.append(data)
		counter += 1
	return np.array(rows)

def load_history():
	return load_history_name('LOGS/history.data')

def load_history_name(fname):
	return np.loadtxt(fname, skiprows=6)

def load_profile(i):
	fname = 'LOGS/profile' + str(i) + '.data'

	rows = []
	counter = 0
	for row in open(fname):
		if counter > 5:
			data = row.split(' ')
			data = list(d for d in data if len(d) > 0)
			data = data[:-1]
			data = list(float(d) for d in data)
			rows.append(data)
		counter += 1

	data = np.array(rows)

	return data