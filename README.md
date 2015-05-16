# disclosure-backend

[![Build Status](https://travis-ci.org/opencalifornia/disclosure-backend?branch=master)](https://travis-ci.org/opencalifornia/disclosure-backend)
[![PyPI version](https://badge.fury.io/py/disclosure-backend.png)](http://badge.fury.io/py/disclosure-backend)
[![Coverage Status](https://coveralls.io/repos/opencalifornia/disclosure-backend/badge.png?branch=master)](https://coveralls.io/r/opencalifornia/disclosure-backend?branch=master)
[![Documentation Status](https://readthedocs.org/projects/disclosure-backend/badge/?version=latest)](https://readthedocs.org/projects/disclosure-backend/?badge=latest)

This repo is OpenCalifornia's fork of the [California Civic Data Coalition][ccdc]'s
[django-calaccess-raw-data](http://django-calaccess-raw-data.californiacivicdata.org/en/latest/)
repository. Whereas django-calaccess-raw-data supports only state-level data, we
aim to add support for importing data from local jurisdictions who use Netfile
to host their data.

## Installation
```
virtualenv env
. env/bin/activate
pip install -r requirements_dev.txt
python example/manage.py downloadcalaccessrawdata --use-test-data
```

## Helpful Links from the CCDC

* Documentation: [django-calaccess-raw-data.californiacivicdata.org](http://django-calaccess-raw-data.californiacivicdata.org)
* Issues: [github.com/opencalifornia/disclosure-backend/issues](https://github.com/opencalifornia/disclosure-backend/issues)
* Packaging: [pypi.python.org/pypi/disclosure-backend](https://pypi.python.org/pypi/disclosure-backend)
* Testing: [travis-ci.org/opencalifornia/disclosure-backend](https://travis-ci.org/opencalifornia/disclosure-backend)
* Coverage: [coveralls.io/r/opencalifornia/disclosure-backend](https://coveralls.io/r/opencalifornia/disclosure-backend)

[ccdc]: http://www.californiacivicdata.org/
