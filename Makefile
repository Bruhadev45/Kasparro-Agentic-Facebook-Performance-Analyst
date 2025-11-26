.PHONY: help setup run test lint clean

help:
	@echo "Kasparro Agentic FB Analyst - Makefile Commands"
	@echo "================================================"
	@echo "make setup    - Install dependencies"
	@echo "make run      - Run analysis (requires QUERY variable)"
	@echo "make test     - Run tests"
	@echo "make lint     - Run linting"
	@echo "make clean    - Clean generated files"

setup:
	python -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt
	@echo "Setup complete! Activate with: source .venv/bin/activate"

run:
ifndef QUERY
	@echo "Usage: make run QUERY='Analyze ROAS drop in last 7 days'"
	@exit 1
endif
	python run.py "$(QUERY)"

test:
	pytest tests/ -v --cov=src

lint:
	flake8 src/ tests/ --max-line-length=100
	black src/ tests/ --check

format:
	black src/ tests/

clean:
	rm -rf reports/*.md reports/*.json logs/*.json
	rm -rf .pytest_cache __pycache__ **/__pycache__ **/*.pyc
	rm -rf .coverage htmlcov/

sample-data:
	head -100 data/synthetic_fb_ads_undergarments.csv > data/sample_fb_ads.csv
	@echo "Sample data created: data/sample_fb_ads.csv"
