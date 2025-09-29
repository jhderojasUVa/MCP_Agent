.PHONY: help run

help:
	@echo "Available commands:"
	@echo "  run    - Run the application. Usage: make run GOOGLE_API_KEY=<your_key>"

run:
ifndef GOOGLE_API_KEY
	$(error GOOGLE_API_KEY is not set. Usage: make run GOOGLE_API_KEY=<your_key>)
endif
	GOOGLE_API_KEY=$(GOOGLE_API_KEY) poetry run python mcp_agent/app.py
