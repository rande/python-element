all: register upload

register:
	python setup.py register

upload:
	python setup.py sdist bdist upload

test:
	cd docs && sphinx-build -nW -b html -d _build/doctrees . _build/html
	nosetests
