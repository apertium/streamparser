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
	coverage report --fail-under 95 --show-missing
	if [[ "$(TRAVIS_PYTHON_VERSION)" != 'pypy'* ]]; then \
		set -e; \
		mypy streamparser.py --strict --any-exprs-report .mypy_coverage; \
		cat .mypy_coverage/any-exprs.txt; \
		coverage=$(shell tail -1 .mypy_coverage/any-exprs.txt | grep -Eo '[0-9\.]+%' | sed 's/%$$//'); \
		if [[ $$coverage < 96 ]]; then \
			echo 'mypy coverage too low'; \
			exit 1; \
		fi \
	fi

distclean:
	rm -rf dist/ build/ *.egg-info/ .mypy_cache/ .mypy_coverage/ .coverage __pycache__/
