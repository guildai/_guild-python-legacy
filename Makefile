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

lint:
	PYTHONPATH=bazel-bin/guild/guild.runfiles/org_pyyaml/lib:bazel-bin/guild/guild.runfiles/org_pocoo_werkzeug pylint guild

clean:
	bazel clean
