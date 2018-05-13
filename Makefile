SHELL := /bin/bash
TRAVIS_PYTHON_VERSION ?= $(shell python3 --version | cut -d ' ' -f 2)

dist:
	python3 setup.py sdist

release:
	python3 setup.py sdist bdist_wheel upload --sign

test-release:
	python3 setup.py sdist bdist_wheel upload --repository https://test.pypi.org/legacy/ --sign

test:
	flake8 *.py --verbose
	coverage run --branch -m unittest test --verbose
	coverage report --fail-under 99 --show-missing
	if [[ "$(TRAVIS_PYTHON_VERSION)" != 'pypy'* ]]; then \
		set -e; \
		mypy streamparser.py --strict --any-exprs-report .mypy_coverage; \
		cat .mypy_coverage/any-exprs.txt; \
		coverage=$$(tail -1 .mypy_coverage/any-exprs.txt | grep -Eo '[0-9\.]+%' | sed 's/%$$//'); \
		exit $$(echo "$${coverage} < 96" | bc -l); \
	fi

distclean:
	rm -rf dist/ build/ *.egg-info/ .mypy_cache/ .mypy_coverage/ .coverage __pycache__/
