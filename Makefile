
build:
	python disclosure-backend/manage.py collectstatic --noinput

run:
	python disclosure-backend/manage.py runserver

test:
	python disclosure-backend/manage.py test

.PHONY: build run test
