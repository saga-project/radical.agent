.PHONY: all docs clean test venv

all: docs

docs:
	make -C docs html

clean:
	-rm -rf build/ dist/ radical*.egg-info/ temp/
	-rm -rf `find . -name \*.egg-info`
	-rm -rf `find . -name \*.egg`
	-rm -rf `find . -name \*.pyc`

venv:
	rm -rf ./venv
	virtualenv ./venv
