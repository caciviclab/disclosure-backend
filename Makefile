
build:
	python manage.py collectstatic --noinput

run:
	python manage.py runserver

test:
	make clean
	flake8 . --exclude cron,migrations,wsgi.py,settings_local.py,env
	coverage run --source='.' manage.py test

clean:
	find . -name \*.pyc -exec rm \{\} \;

.PHONY: build run test
