RUN := uv --offline run

.PHONY: check
check:
	@$(RUN) ruff format --check && \
		$(RUN) ruff check && \
		$(RUN) ty check

.PHONY: format
format:
	@$(RUN) ruff format && \
		$(RUN) ruff check --fix --select I,Q
