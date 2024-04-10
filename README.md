# Scrape Away

## Description
The web application provides a low code web scraping utility. The web application is created using flask while the scraper hidden within is based on the requests libary.

## Table Of Contents

-[Installation](#Installation)

-[Usage](#Usage)

## Installation

- Create a root folder and import the repository.
- Create virtual environment using the command ```python-m venv <path_to_the_root_folder>``` and activate it using the command ```venv\Scripts\activate```.
- Download the requirements by running the command ```python -m pip install -r requirements.txt```
- Run the command ```python -m flask --app flaskr init-db```. This will initialize an sqlite instance which will be used to store user info.
- Run the command ```python -m flask --app flaskr run```. This will start the web application. The command line will provide url link for the web application.  

## Usage
