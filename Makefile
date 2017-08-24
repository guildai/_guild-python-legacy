GUILD = bazel-bin/guild/guild

.PHONY: build
build:
	bazel build guild

component-deps: components/.deps-resolved

components/.deps-resolved:
	bower install
	scripts/patch-components
	touch components/.deps-resolved

check: $(GUILD)
	@if [ -z "$(TESTS)" ]; then \
	  opts="--all-tests"; \
	else \
	  opts=""; \
	  for test in $(TESTS); do \
	    opts="$$opts --test $$test"; \
	  done; \
	fi; \
	$(GUILD) check $$opts; \

check3:
	python3 scripts/test $(TESTS)

lint:
	pylint guild

lint3:
	pylint3 guild

clean:
	bazel clean
