
build:
	python manage.py collectstatic --noinput

run:
	python manage.py runserver

test:
	python manage.py test

.PHONY: build run test
