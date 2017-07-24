.PHONY: build
build:
	@echo "Use 'sudo make install' to install dependencies and link to this project"

install:
	python setup.py develop

check:
	scripts/test $(TESTS)

lint:
	pylint guild
