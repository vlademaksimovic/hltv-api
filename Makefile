.PHONY: install start test

install:
	pip install -r requirements.txt

start:
	python3 src/app.py

test:
	pushd test; pytest; popd

