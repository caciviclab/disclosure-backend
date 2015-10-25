[![Build
Status](https://travis-ci.org/caciviclab/disclosure-backend.svg?branch=master)](https://travis-ci.org/caciviclab/disclosure-backend)

California Civic Lab Disclosure Backend
==================================================
[![Mockup](/mockups/odca-mobile-09-ballot_measure-small.jpeg)](/mockups/odca-mobile-09-ballot_measure.jpeg)
[![Mockup](/mockups/odca-mobile-09-ballot_measure 2-small.jpeg)](/mockups/odca-mobile-09-ballot_measure 2.jpeg)
[![Mockup](/mockups/odca-mobile-09-ballot_measure 3-small.jpeg)](/mockups/odca-mobile-09-ballot_measure 3.jpeg)
[![Mockup](/mockups/odca-mobile-09-ballot_measure 4-small.jpeg)](/mockups/odca-mobile-09-ballot_measure 4.jpeg)
[![Mockup](/mockups/odca-mobile-09-ballot_measure 5-small.jpeg)](/mockups/odca-mobile-09-ballot_measure 5.jpeg)
[![Mockup](/mockups/odca-mobile-09-ballot_measure 6-small.jpeg)](/mockups/odca-mobile-09-ballot_measure 6.jpeg)
[![Mockup](/mockups/odca-mobile-09-ballot_measure 7-small.jpeg)](/mockups/odca-mobile-09-ballot_measure 7.jpeg)
[![Mockup](/mockups/odca-mobile-09-ballot_measure 8-small.jpeg)](/mockups/odca-mobile-09-ballot_measure 8.jpeg)

## Dependencies

If you've worked with Django and python before, these steps should be familiar to you.
We're going to create an environment with Python 2.7.9 for the project

## Clone it to your system

First, clone `disclosure-backend` (or your fork of it) to your own local copy.

## Setup

1. Install python and pip (if using Anaconda, pip is already installed)
2. Create an environment for this project:
  * For non-Anaconda Python distribution 
    ```
    sudo pip install virtualenv
    virtualenv env
    source env/bin/activate
    ```

  * For Anaconda (we'll make an environment called ODB with Python 2.7.9 in it)
    ```
    conda create --name ODB python=2.7.9
    source activate ODB
    ```

  (you will have to activate this environment (or virtualenv) every time you want to start working)

3. Install project requirements with:
   `pip install -r requirements.txt`

4. install mysql 
  * When prompted for a password, remember it because you'll need it.

### MySQL

#### Install mysql

```
    Mac: brew install mysql
```

#### Prepare the database

```
mysql --user root
mysql> create database calaccess_raw;
mysql> \q
python disclosure-backend/manage.py migrate
```
(If mysql exits with a complaint about a password, use `mysql -p --user root`)


#### Modify `settings.py` (or create `settings_local.py`)
In `disclosure-backend/project/settings.py` you'll find the database specification 
```
DATABASES = {
    'default': {
        'NAME': 'calaccess_raw',
        'PASSWORD': '',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'local_infile': 1,
        }
    }
```
Change the password field to the password you chose when you installed MySQL. 
Alterntively, you can copy `settings.py` to `settings_local.py` and modify that local version of it.
django will use `settings_local.py` if it's there.


## Run the tests

    $ make test

It should load and clean some files in a few seconds.

## Download the data

First, a basic data check to make sure things are working:

    $ python disclosure-backend/manage.py downloadcalaccessrawdata --use-test-data
(this appears to do the same thing as `make test`)

### Zipcode/metro data

    $ python disclosure-backend/manage.py downloadzipcodedata

### Netfile

Netfile contains campaign finance data for a number of jurisdictions. Not all
jurisdictions will have data.

    $ python disclosure-backend/manage.py downloadnetfilerawdata

### Cal-Access

Cal-Access is the state data. It's ~750MB of data and takes over an hour to
trim, clean and process.

    $ python disclosure-backend/manage.py downloadcalaccessrawdata

## Deploying

```
ssh opencal.opendisclosure.io /usr/local/bin/deploy-backend
```

To run for the purposes of development, accessing Django's admin interface:

```
python disclosure-backend/manage.py createsuperuser
< and create a username/password for yourself>

python disclosure-backend/manage.py runserver
```

Then go to http://127.0.0.1:8000/admin to log in and see data.

