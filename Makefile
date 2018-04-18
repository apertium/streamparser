dist:
	python3 setup.py sdist

release:
	python3 setup.py sdist bdist_wheel upload --sign

test-release:
	python3 setup.py sdist bdist_wheel upload --repository https://test.pypi.org/legacy/ --sign

test:
	flake8 *.py
	coverage run --branch -m unittest test
	coverage report --fail-under 95
	mypy streamparser.py --strict

distclean:
	rm -rf dist/ build/ *.egg-info/ .mypy_cache/ .coverage __pycache__/
