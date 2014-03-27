all: test doc dev

package: register upload

register:
	python setup.py register

upload:
	python setup.py sdist bdist upload

test:
	nosetests
	cd element/standalone/skeleton && nosetests

doc:
	cd docs && sphinx-build -nW -b html -d _build/doctrees . _build/html

dev:
	cd element/standalone/skeleton && python start.py tornado:start --verbose

prod:
	cd element/standalone/skeleton && python start.py tornado:start -np 8

fixtures:
	cd element/standalone/skeleton && python start.py element:demo:fixtures
