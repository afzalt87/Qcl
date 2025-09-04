# Makefile for QCL Local Development

.PHONY: help setup install clean test run-sample run validate format

# Default target
.DEFAULT_GOAL := help

# Variables
PYTHON := python3
PIP := pip3

help: ## Show this help message
	@echo "QCL - Simple Local Development Commands"
	@echo "======================================"
	@echo "Available commands:"
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ { printf "  %-15s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

setup: ## Create project structure and virtual environment
	@echo "Setting up QCL project structure..."
	@mkdir -p src/qcl/{core,data,pipeline,classification}
	@mkdir -p data/input/{queries,guidelines,images}
	@mkdir -p data/{processed,output}
	@mkdir -p {scripts,configs,tests,logs}
	@echo "Creating virtual environment..."
	@$(PYTHON) -m venv .venv
	@echo "✓ Project structure created!"
	@echo "Next steps:"
	@echo "1. source .venv/bin/activate  (or .venv\\Scripts\\activate on Windows)"
	@echo "2. make install"
	@echo "3. cp .env.example .env (and edit with your OpenAI API key)"

install: ## Install dependencies
	@echo "Installing dependencies..."
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt
	@echo "✓ Dependencies installed!"

clean: ## Clean up temporary files
	@echo "Cleaning up..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@rm -rf .pytest_cache/
	@rm -f logs/*.log
	@echo "✓ Cleanup completed!"

test: ## Run basic tests
	@echo "Running tests..."
	@$(PYTHON) -m pytest tests/ -v || echo "No tests found - that's okay for now"

validate: ## Validate your setup and data
	@echo "Validating setup..."
	@$(PYTHON) scripts/run_classification.py validate \
		--queries data/input/queries/test_queries.csv || echo "Create your queries file first"

run-sample: ## Run classification on sample data
	@echo "Running sample classification..."
	@$(PYTHON) scripts/run_classification.py classify \
		--queries data/input/queries/test_queries.csv \
		--guidelines data/input/guidelines/QG.pdf \
		--output data/output/sample_results.json \
		--max-queries 5

run: ## Run full classification
	@echo "Running full classification..."
	@$(PYTHON) scripts/run_classification.py classify \
		--queries data/input/queries/test_queries.csv \
		--guidelines data/input/guidelines/QG.pdf \
		--output data/output/results.json

format: ## Format code (optional)
	@echo "Formatting code..."
	@black src/ scripts/ --line-length 120 || echo "Black not installed - skip with: pip install black"
	@isort src/ scripts/ || echo "isort not installed - skip with: pip install isort"

check-config: ## Check if configuration is working
	@echo "Checking configuration..."
	@$(PYTHON) -c "from src.qcl.core.config import get_config; cfg = get_config(); print('✓ Config loaded successfully'); print(f'Environment: {cfg.environment}'); print(f'OpenAI key set: {bool(cfg.openai_api_key and cfg.openai_api_key != \"your_openai_api_key_here\")}')"

create-sample-data: ## Create sample data files for testing
	@echo "Creating sample data..."
	@mkdir -p data/input/queries
	@echo "query" > data/input/queries/test_queries.csv
	@echo "best restaurants near me" >> data/input/queries/test_queries.csv
	@echo "weather today" >> data/input/queries/test_queries.csv
	@echo "how to cook pasta" >> data/input/queries/test_queries.csv
	@echo "iphone 15 price" >> data/input/queries/test_queries.csv
	@echo "taylor swift" >> data/input/queries/test_queries.csv
	@echo "✓ Sample queries created in data/input/queries/test_queries.csv"
	@echo "Note: You still need to add your guidelines PDF file to data/input/guidelines/"

view-results: ## View the latest results
	@echo "Latest results:"
	@ls -la data/output/ 2>/dev/null || echo "No results yet - run 'make run-sample' first"
	@echo ""
	@echo "To view JSON results nicely formatted:"
	@echo "cat data/output/sample_results.json | python -m json.tool"

logs: ## View recent logs
	@echo "Recent log entries:"
	@tail -20 logs/qcl.log 2>/dev/null || echo "No logs yet"

status: ## Show project status
	@echo "QCL Project Status"
	@echo "=================="
	@echo "Project structure:"
	@ls -la data/input/ 2>/dev/null || echo "  ✗ No input data directory"
	@echo ""
	@echo "Required files:"
	@test -f data/input/queries/test_queries.csv && echo "  ✓ Queries file exists" || echo "  ✗ Queries file missing (run 'make create-sample-data')"
	@test -f data/input/guidelines/QG.pdf && echo "  ✓ Guidelines PDF exists" || echo "  ✗ Guidelines PDF missing (add your PDF file)"
	@test -f .env && echo "  ✓ Environment file exists" || echo "  ✗ .env file missing (copy from .env.example)"
	@echo ""
	@echo "Virtual environment:"
	@test -d .venv && echo "  ✓ Virtual environment exists" || echo "  ✗ Virtual environment missing (run 'make setup')"
	@echo ""
	@echo "Results:"
	@test -f data/output/sample_results.json && echo "  ✓ Sample results exist" || echo "  ✗ No sample results (run 'make run-sample')"

# Quick start workflow
quick-start: setup install create-sample-data ## Complete quick start setup
	@echo ""
	@echo "🎉 Quick start completed!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Activate virtual environment: source .venv/bin/activate"
	@echo "2. Copy and edit environment file: cp .env.example .env"
	@echo "3. Add your OpenAI API key to the .env file"
	@echo "4. Add your guidelines PDF to: data/input/guidelines/QG.pdf"
	@echo "5. Test the setup: make run-sample"
	@echo ""
	@echo "For help: make help"

convert-csv: ## Convert JSON results to CSV
	@python scripts/json_to_csv.py