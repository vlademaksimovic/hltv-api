.PHONY: ci install start lint test

ci: install lint test

install:
	pip install -r requirements.txt

start:
	python3 src/app.py

lint:
	pep8 --format=pylint src test

test:
	pushd test; pytest; popd
