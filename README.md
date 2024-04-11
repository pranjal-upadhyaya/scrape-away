# Scrape Away

## Description
The web application provides a low code web scraping utility. The user can enter the URL and once the page source is scraped use the data mining functionality provided to mine data from the page source. The web application is created using flask while the scraper hidden within is based on the requests library. The data mining functionality is implemented using Beautiful Soup.

## Table Of Contents

-[Achievements](#Achievements)

-[Future Goals](#Goals)

-[Installation](#Installation)

-[Usage](#Usage)

## Achievements

- A basic authentication system has been implemented that allows the user to register, login and logout from the web framework.
- The web scraping and data mining functionalities are made available only to users who are logged in. 
- A web framework has been provided where the user can enter a url and scrape its webpage.
- Once the webpage is successfully scraped, the framework provides the user with the capability to mine data from the scraped page source.
- The configuration used can be saved and recalled later to mine page sources.

## Goals

- Add the feature to store and download scraped data.
- Add the feature to allow users to feed a csv of urls and specify a saved mining configuration. The backend process will then mine data from the page source of each url in the csv and save the mined data for future retrieval.
- Add a credit system that binds the number of data rows that can be downloaded to the number of credits available in a users account.
- Add OTP authentication to the registration process.
- Containarize the entire framework using Docker.

## Installation

- Create a root folder and import the repository.
- Create virtual environment using the command ```python-m venv <path_to_the_root_folder>``` and activate it using the command ```venv\Scripts\activate```.
- Download the requirements by running the command ```python -m pip install -r requirements.txt```
- Run the command ```python -m flask --app flaskr init-db```. This will initialize an sqlite instance which will be used to store user info.
- Run the command ```python -m flask --app flaskr run```. This will start the web application. The command line will provide url link for the web application.  

## Usage
