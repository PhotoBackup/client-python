all: bootstrap

bootstrap:
	[ -e ./venv/bin/pip ] || virtualenv venv
	./venv/bin/pip install blessings docopt requests
