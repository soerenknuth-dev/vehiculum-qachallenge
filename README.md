# vehiculum QA Challenge

The task is to design and implement a small automation testing tool to check small functionalities on Vehiculum Homepage.
The Tests are checking the functionality of the Search, Hot-Offers and Brand-Slider on desktop and mobile views.
This tool is written in Python using the Pytest framework. It is using Python bindings for Selenium and ChromeDriver.

## Prerequisites

* download and install [Python 3](https://www.python.org/downloads/)
* download the matching version of [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) for Chrome installed
* Make sure both is in your PATH

## Installing

* clone repository https://github.com/soerenknuth-dev/vehiculum-qachallenge.git
* run ```pip install pipenv``` to install pipenv dependency manager
* run ```pipenv install --dev``` to install dev dependencies

This requires Python 3.8, if you have an older version just edit the Pipfile and Pipfile.lock

## Running the test

* to run all the tests found in subfolder /tests:

```pipenv run python -m pytest --html=report.html```

* to run only mobile test:

```pipenv run python -m pytest tests/test_homepage_mob.py --html=report.html```

* to run a specific test:

```pipenv run python -m pytest tests/test_homepage_mob.py::test_homepage_search_mobile --html=report.html```

After completion a report (report.html) can be found in the directory.

## Built with
* [Python 3](https://www.python.org/downloads/)
* [Pytest](https://docs.pytest.org/en/latest/) - Python testing framework
* [pipenv](https://github.com/pypa/pipenv) - package and virtualenv management
* [Selenium with Python](https://selenium-python.readthedocs.io/) - Python bindings for Selenium
* [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) - WebDriver interface for Chrome

### Todos
* create page object models and move locators and methods
* refactor locators
* checks in more browsers maybe using saucelabs or browserstack
* extend asserts
