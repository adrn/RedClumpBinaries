all: cache/parsed.data cache/q_fits.data cache/fr_fits.data

cache/parsed.data: parse_binaries.py
	python parse_binaries.py

cache/q_fits.data: cache/parsed.data config.py fit_q.py slice_helpers.py fit_helpers.py
	python fit_q.py

cache/fr_fits.data: cache/parsed.data cache/q_fits.data fit_fr.py

clean:
	rm cache/*.data
