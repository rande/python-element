all: test doc dev

package: register upload

register:
	python setup.py register

upload:
	python setup.py sdist bdist upload

test:
	nosetests
	cd element/standalone/skeleton && nosetests

install:
	pip install -r requirements_test.txt
	cd element/standalone/skeleton && bower update

doc:
	cd docs && sphinx-build -nW -b html -d _build/doctrees . _build/html

dev:
	cd element/standalone/skeleton && python start.py tornado:start --verbose -d --bind element.vagrant:5000

prod:
	cd element/standalone/skeleton && python start.py tornado:start -np 8

bower:
	cd element/standalone/skeleton && bower update

fixtures:
	cd element/standalone/skeleton && python start.py element:demo:fixtures
