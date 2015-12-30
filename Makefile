
build:
	python manage.py collectstatic --noinput

run:
	python manage.py runserver

test:
	flake8 . --exclude cron,migrations,wsgi.py,env
	coverage run --source='.' manage.py test

.PHONY: build run test
