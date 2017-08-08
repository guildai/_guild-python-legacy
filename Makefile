.PHONY: build
build:
	@echo "Use 'sudo make install' to install dependencies and link to this project"

install:
	python setup.py develop

component-deps: components/.deps-resolved

components/.deps-resolved:
	bower install
	scripts/patch-components
	touch components/.deps-resolved

check:
	scripts/test $(TESTS)

lint:
	pylint guild
