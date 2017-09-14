GUILD = bazel-bin/guild/guild

build:
	bazel build guild

component-deps: components/.deps-resolved

components/.deps-resolved:
	bower install
	scripts/patch-components
	touch components/.deps-resolved

check: $(GUILD)
	@if [ -z "$(TESTS)" ]; then \
	  opts="--tests"; \
	else \
	  opts="-s "; \
	  for test in $(TESTS); do \
	    opts="$$opts -t $$test"; \
	  done; \
	fi; \
	$(GUILD) check $$opts; \

lint:
	PYTHONPATH=bazel-bin/guild/guild.runfiles/org_pyyaml/lib:bazel-bin/guild/guild.runfiles/org_psutil:bazel-bin/guild/guild.runfiles/org_pocoo_werkzeug:bazel-bin/guild/gpkg.runfiles/org_semantic_version pylint -rn guild

clean:
	bazel clean

commit-check:
	make
	make check
	make lint
