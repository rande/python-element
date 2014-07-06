all: test doc dev

package: register upload

register:
	python setup.py register

upload:
	python setup.py sdist bdist upload

test:
	nosetests
	cd element/standalone/skeleton && nosetests
	cd docs && sphinx-build -nW -b html -d _build/doctrees . _build/html
	#for f in $$(find . -name '*.py'); do pyflakes $$f; done

install:
	pip install -r requirements_test.txt
	cd element/standalone/skeleton && bower install

doc:
	cd docs && sphinx-build -nW -b html -d _build/doctrees . _build/html

dev:
	cd element/standalone/skeleton && python start.py tornado:start --verbose -d --bind element.vagrant

proxy:
	cd element/standalone/skeleton && python proxy.py 5000

prod:
	cd element/standalone/skeleton && python start.py tornado:start -np 8

bower:
	cd element/standalone/skeleton && bower install

fixtures:
	cd element/standalone/skeleton && python start.py element:demo:fixtures
