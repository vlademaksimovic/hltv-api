.PHONY: ci build deploy dev install start lint test test-cov

# Travis cannot use 'pushd' or 'popd' without SHELL defined
SHELL := /bin/bash
IMAGE_NAME = hltv-api

ci: install lint unzip test

build:
	docker build -t $(IMAGE_NAME):latest .

deploy: lint test build
	heroku container:push web

dev:
	python3 app.py

install:
	pip install -r requirements.txt

start:
	docker run -p 8000:8000 --restart=always $(IMAGE_NAME):latest

lint:
	pep8 --format=pylint src test

test:
	pushd test; pytest; popd

test-cov:
	pushd test; py.test --cov-report=html:../coverage --cov-report=term --no-cov-on-fail --cov src; popd

zip:
	pushd test; tar -zcvf resources.tar.gz resources; popd

unzip:
	pushd test; tar -zxvf resources.tar.gz; popd

