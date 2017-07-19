.PHONY: build
build:
	python setup.py develop

check:
	scripts/test
