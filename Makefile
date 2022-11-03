export NOTION_DB_IMAGES=${NOTION_DB_DEVELOP}
# export NOTION_DB_IMAGES=${NOTION_DB_NAI_DIFFUSION}

default:
	python -m miru

debug:
	python -m miru -v

test:
	python -m unittest discover tests

cli:
	python -m miru.cli
