# Scraped NEWS sentiment analysis

## Environment activation:
* python -m venv env
* env\Scripts\activate.bat
* pip install -r requirements.txt

## Project create:
* django-admin startproject news_sentiment_feedback

## App create:
* python manage.py startapp news_sentiment_analyzer

## Project tree:
|_ settings.py for project settings, app, database, templates, authentication, middleware manage
|_ urls.py for project router path adjust

## App tree:
|_ admin.py for admin panel site view modification
|_ models.py for object relational mapping(ORM) database create
|_ urls.py for app router path adjust 
|_ views.py for templates/api view modification

## Predictor:
|_ news_predictor.py for found news sentiment analysis model setup

## Scraper:
|_ news_scraper.py for news scraping through online site

## Database migrations:
* python manage.py makemigrations
* python manage.py migrate

## Super-user creation:
* python manage.py createsuperuser