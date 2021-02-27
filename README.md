# Twitter Streaming Flask App

## Introduction
This backend application implements a Flask REST API as well as the Twitter API to stream tweets in real-time for a given topic and interval of time requested by the client (in this case, requests from Postman, Insomnia, etc). After registration and login, a POST request is made to a Flask endpoint which will then activate a stream listener for a list of topics given in the request body. The tweets are then stored in a Redis cache and a PostgresQL database.

## Tech Stack Used
* Flask (w/ Python 3.8.5)
* Flask-JWT
* Tweepy + Twitter API
* SQLAlchemy
* PostgresQL
* Redis

## Installation
Clone the repo.
`git clone https://github.com/KristianS1991/backend-project.git`

Create virtual environment.
`virtualenv venv --python=python3`

Activate virtual environment.
`source venv/bin/activate`

Install dependencies.
`pip install -r requirements.txt`

Sign up for a twitter developer account. Once approved, create a new app in the console and copy the `consumer_key` , `consumer_secret` , `access_token` , `access_token_secret` API keys. Paste these keys in a JSON object in a file at location `twitter/api_config.json` within your top-level directory. Don't forget to add this file to your `.gitignore`.


## Running the application
Activate virtual environment.
`source venv/bin/activate`

To start the flask server.
`python app.py`

To start the redis server.
`redis-6.0.10/src/redis-server`

Make requests to the flask endpoints from a client such as Postman, Insomnia, etc.

## WIP
Install and setup celery as a Task Queue with a RabbitMQ broker. Implement RabbitMQ publish/subscribe functionality.
