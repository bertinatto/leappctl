.PHONY: clean
clean:
	@rm -rf build/ dist/ *.egg-info
	@find . -name '__pycache__' -exec rm -fr {} +
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +

.PHONY: build
build:
	true

.PHONY: install-deps
install-deps:
	pip install -r requirements.txt

.PHONY: install
install:
	python setup.py install

.PHONY: test
test:
	py.test tests/*.py
