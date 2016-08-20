
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

deploy.pem: deploy.pem.enc .travis.yml
	openssl aes-256-cbc -K ${encrypted_997553aff5ab_key} -iv ${encrypted_997553aff5ab_iv} -in deploy.pem.enc -out deploy.pem -d
	chmod 600 deploy.pem

deploy: deploy.pem
	ssh -o UserKnownHostsFile=./deploy.known_hosts \
		-i deploy.pem \
		backend@admin.caciviclab.org \
		/usr/local/bin/deploy-backend

.PHONY: build run test
