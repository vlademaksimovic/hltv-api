.PHONY: install start-app start-env

install:
	pip install -r requirements.txt

start:
	python3 ./src/app.py
