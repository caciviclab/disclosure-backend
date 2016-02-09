This project has a number of non-obvious aspects to contributing; this document is designed to outline the issues!

## Project overview

Technical docs are kept in our wiki. Important docs to be familiar with include:
* A [glossary of terms](https://github.com/caciviclab/caciviclab.github.io/wiki/Glossary) we use in the app. Use these for naming variables, functions, and objects in the code.
* An [outdated schema](https://github.com/caciviclab/caciviclab.github.io/wiki/Data-relationships---Database-schema) of the database/model structure. 
* A simple [technical overview](https://github.com/caciviclab/caciviclab.github.io/wiki/Technical-Overview) of the project

Non-technical docs are also available to understand the complex space of campaign finance. These include:
* A [campaign finance summary](https://github.com/caciviclab/caciviclab.github.io/wiki/Campaign-Finance)


## Testing code changes

There are three different ways for users interact with this code; for two, documentation and output strings become very important. Each must be tested independently for verification.

#### API via frontend

This repository defines a backend API for disclosure data. The goal is to support any front-end, but we currently focus on [our own frontend](https://github.com/caciviclab/disclosure-frontend). 

**Testing: automated**
Run `make test` from the project root to run existing tests. 

When making any changes to the API schema (the API endpoints, and/or the JSON format produced by any endpoint), please:
* Update and/or add automated tests.
* Test on our frontend repository and make relevant changes (or, at the minimum, post a new issue to the frontend repo).

#### Swagger UI

In addition to being machine-readable, we also want our API to be human-readable. For that reason, we use Swagger to document our API. When adding/updating the API schema, please check that the documentation exposed by Swagger is clear, complete, and correct.

**Testing: manual**
Locally, verify Swagger documentation manually at http://127.0.0.1:8000/docs/ before submitting PRs that change the API schema.

#### Admin Interface

We have non-technical users who review, modify, and add data through the admin interface. This means that all models must have meaningful docstrings and `__str__` functions (so that humans can understand what a model instance refers to in the admin list view), and model fields must have useful `help_text` functions.

**Testing: manual**
Locally, verify your model changes manually via http://127.0.0.1:8000/admin/ before submitting PRs that change the model schema. 


## Style Guide

* `flake8` is installed via `requirements_dev.txt` and is run in our tests to maintain a `pep8`-consistent codebase.
* Docstrings in views are used by the Django `rest-framework` and `django-swagger` packages, please see the links for details.

