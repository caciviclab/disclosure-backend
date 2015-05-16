.PHONY: bootstrap install install-yes docs load rs sh test

bootstrap:
	mysqladmin -h localhost -u root -pmysql drop calaccess
	mysqladmin -h localhost -u root -pmysql create calaccess
	python example/manage.py syncdb
	python example/manage.py downloadcalaccessrawdata
	python example/manage.py collectstatic --noinput
	python example/manage.py runserver

install:
	python setup.py sdist
	/usr/local/bin/pip uninstall django-calaccess-raw-data
	/usr/local/bin/pip install --user dist/django-calaccess-raw-data-0.1.2.tar.gz

install-yes:
	python setup.py sdist
	/usr/local/bin/pip uninstall django-calaccess-raw-data --yes
	/usr/local/bin/pip install --user dist/django-calaccess-raw-data-0.1.2.tar.gz

install-only:
	python setup.py sdist
	/usr/local/bin/pip install --user dist/django-calaccess-raw-data-0.1.2.tar.gz

docs:
	cd docs && make livehtml

load:
	python example/manage.py downloadcalaccessrawdata --skip-download --skip-unzip --skip-prep --skip-clear --skip-clean

rs:
	python example/manage.py runserver

sh:
	python example/manage.py shell

test:
	pep8 calaccess_raw
	pyflakes calaccess_raw
	coverage run example/manage.py test calaccess_raw
	coverage report -m
