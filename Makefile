GUILD = bazel-bin/guild/guild

build: build-guild build-gpkg

build-guild:
	bazel build guild:guild

build-gpkg:
	bazel build guild:gpkg

component-deps: components/.deps-resolved

components/.deps-resolved:
	bower install
	scripts/patch-components
	touch components/.deps-resolved

check: $(GUILD)
	@if [ -z "$(TESTS)" ]; then \
	  opts="--tests"; \
	else \
	  opts=""; \
	  for test in $(TESTS); do \
	    opts="$$opts -t $$test"; \
	  done; \
	fi; \
	$(GUILD) check $$opts; \

lint:
	PYTHONPATH=bazel-bin/guild/guild.runfiles/org_pyyaml/lib:bazel-bin/guild/guild.runfiles/org_psutil:bazel-bin/guild/guild.runfiles/org_pocoo_werkzeug pylint -rn guild

clean:
	bazel clean

commit-check:
	make
	make check
	make lint
