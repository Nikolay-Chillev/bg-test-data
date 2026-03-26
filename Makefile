.PHONY: test coverage lint format typecheck report build clean install

test:
	pytest -v

coverage:
	pytest --cov=bg_test_data --cov-report=html

lint:
	ruff check src/ tests/

format:
	ruff format src/ tests/

typecheck:
	mypy src/bg_test_data/

report:
	allure serve allure-results

build:
	python -m build

clean:
	rm -rf dist/ build/ *.egg-info src/*.egg-info
	rm -rf .coverage htmlcov/ coverage.xml
	rm -rf allure-results/ allure-report/
	rm -rf .pytest_cache/ .mypy_cache/ .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

install:
	pip install -e ".[dev]"
