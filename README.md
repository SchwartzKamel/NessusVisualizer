# NessusVisualizer

Web application to visualize Nessus scan results in a concise, succinct fashion.

## Getting Started

### Prerequisites

This app was built with the following:

```
Ubuntu 20.04
Python 3.8
```

You will need to setup a [Nessus scanner](https://www.tenable.com/products/nessus), and have at least one scan result.

Additionally, you will need to setup a [RedisLabs](https://redislabs.com/try-free/) account

### Installing

Clone the application (git clone or download and unpack the zip) and create your virtual environment (or install Poetry and use `poetry shell`)

Install the dependencies

```
pip install -r requirements.txt
```

Run the setup script

```
python setup.py
```

Answer the prompts to configure the .env file

In case you want to create this file manually, use the below template (DEV_DATABASE_URI is optional)

```
SECRET_KEY=<RANDOM_STRING>
FLASK_APP=wsgi.py
PROD_DATABASE_URI=sqlite:////<FULL_PATH_TO_FILE>
DEV_DATABASE_URI=sqlite:////<FULL_PATH_TO_FILE>
SESSION_TYPE=redis
REDIS_URI=redis://:[password]@[host_url]:[port]
NESSUS_URL=https://<NESSUS_SCANNER_IP>:8834
NESSUS_USER=<SCANNER_USERNAME>
NESSUS_PASS=<SCANNER_PASSWORD>
```

Start the server

```
python wsgi.py
```

### Deployment

You can pass this project to Gunicorn 3, uWSGI, Waitress, etc. and for extending testing, install tmux and start the server from there.

## Usage

End with an example of getting some data out of the system or using it for a little demo
![icon](app/static/img/favicon.ico)
