PYTHON ?= python3
VENV ?= .venv
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest
STREAMLIT := $(VENV)/bin/streamlit

.PHONY: setup test run format clean

setup:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

test:
	$(PYTEST) -q

run:
	$(STREAMLIT) run app.py

clean:
	rm -rf $(VENV) .pytest_cache
