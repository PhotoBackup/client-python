all: bootstrap

bootstrap:
	[ -e ./venv/bin/pip ] || pyvenv venv
	./venv/bin/pip install blessings docopt requests
