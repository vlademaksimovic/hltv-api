# Contributing
The following is a set of guidelines for contributing to hltv-api. **This
project is written using Python version 3.6.**

## Setup dev environment
The recommended setup is using `virtualenv` for development. To be sure that your
virtual environment is using the correct version you might have to do
something like this when you create it:

```bash
mkvirtualenv --python=`which python3` hltv-api
```

This should be the only "raw" command you have to enter, the rest of them
should be existing make targets. If you find something useful that's not -
please submit a pull request with it.

### Install dependencies
```bash
make install
```

### Start local server
To start a local Flask server:

```bash
make dev
```

To make sure that the server is up and running:

```bash
curl http://0.0.0.0:8000/
```

## Run tests
If it's the first time you're running them, make sure to unrar all the test
resource files by running:

```bash
make unzip
```

After that you can just run:

```bash
make test
```

## Linting
Travis won't accept your pull request unless it passes linting, so make sure
to run it before submitting your pull request.

```bash
make lint
```
