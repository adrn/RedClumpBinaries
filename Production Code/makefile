all: cache/parsed.data cache/q_fits.data cache/fr_fits.data cache/mesa_parsed.data

cache/parsed.data: parse_binaries.py
	python parse_binaries.py

cache/mesa_parsed.data: parse_mesa.py
	python parse_mesa.py

cache/q_fits.data: cache/parsed.data config.py fit_q.py slice_helpers.py fit_helpers.py
	python fit_q.py

cache/fr_fits.data: cache/parsed.data cache/q_fits.data fit_fr.py mesa_helpers.py
	python fit_fr.py

clean:
	rm cache/*.data
