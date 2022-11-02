default:
	python -m miru

debug:
	python -m miru -v

test:
	python -m unittest discover tests

cli:
	python -m miru.cli
