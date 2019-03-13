.PHONY: clean clean-virtualenv virtualenv build test

clean:
	@find . -name '*.py[co]' -delete
	@rm -rf .coverage
	@rm -f TEST-*.xml
	@rm -f COVERAGE-*.xml
	@rm -f flake8.txt
	@echo "Workspace clean"

clean-virtualenv:
	@rm -rf .venv
	@echo "Virtual env removed."

virtualenv:
	@if [ ! -d "./.venv" ]; then \
		curl -s https://bootstrap.pypa.io/get-pip.py -o get-pip.py; \
		python3 --version; \
		python3 get-pip.py --user; \
		pip3 install virtualenv; \
		python3 -m venv .venv; \
	fi

build: virtualenv
	@. .venv/bin/activate; \
	pip install -r requirements.txt;

test: virtualenv
	. .venv/bin/activate; \
	pip install -r requirements-dev.txt; \
	pytest --verbose --cov=a2_cli --cov-report term tests; \
	pytest --verbose --cov=a2_cli --cov-report term integration; \
	flake8 --statistics --show-source a2_cli tests integration || true;
