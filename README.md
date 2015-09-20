California Civic Lab Disclosure Backend
==================================================

## Setup

1. Install python and pip
2. `sudo pip install virtualenv`
3. `virtualenv env`
4. `source env/bin/activate` (you will have to do this every time you want to
   start working)
5. `pip install -r requirements.txt`
6. install mysql

## Dependencies

If you've worked with Django and python before, these steps should be familiar to you.

### Virtualenv

You'll need python, pip, virtualenv.

#### Mac

Python 2.7.9 includes pip:

```
brew install python
pip install virtualenv
```

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


## Download the data

First, a basic data check to make sure things are working:

    $ python disclosure-backend/manage.py downloadcalaccessrawdata --use-test-data

### Zipcode/metro data

    $ python disclosure-backend/manage.py downloadzipcodedata

### Netfile

Netfile contains campaign finance data for a number of jurisdictions. Not all
jurisdictions will have data.

    $ python disclosure-backend/manage.py downloadnetfilerawdata

### Cal-Access

Cal-Access is the state data. It's ~750MB of data and takes about an hour to
trim, clean and process.

    $ python disclosure-backend/manage.py downloadcalaccessrawdata

## Deploying

```
ssh opencal.opendisclosure.io /usr/local/bin/deploy-backend
```
