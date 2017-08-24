.PHONY: build
build:
	bazel build guild

install:
	python setup.py develop

install3:
	python3 setup.py develop

component-deps: components/.deps-resolved

components/.deps-resolved:
	bower install
	scripts/patch-components
	touch components/.deps-resolved

check:
	python2 scripts/test $(TESTS)

check3:
	python3 scripts/test $(TESTS)

lint:
	pylint guild

lint3:
	pylint3 guild

clean:
	bazel clean
