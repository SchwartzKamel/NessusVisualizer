"""Script to setup app environment"""
import os


def env_writer(setting_name, question):
    user_input = input(question)
    environment.write(setting_name + "=" + user_input)


def env_db_writer(setting_name, question):
    user_input = input(question)
    environment.write(setting_name + "=sqlite:///" + user_input)


with open(".env", 'w') as environment:
    # SECRET_KEY
    key = os.urandom(16)
    environment.write("SECRET_KEY=" + key)
    # FLASK_APP
    environment.write("FLASK_APP=wsgi.py")
    # PROD_DATABASE_URI
    env_db_writer("PROD_DATABASE_URI",
                  "What is the path to the prod database?")
    # SESSION_TYPE
    environment.write("SESSION_TYPE=redis")
    # REDIS_URI
    env_writer("REDIS_URI", "What is your Redis URI?")
    # NESSUS_URL
    env_writer("NESSUS_URL", "What is the IP of your Nessus scanner?")
    # NESSUS_USER
    env_writer("NESSUS_USER", "What is the username for your Nessus scanner?")
    # NESSUS_PASS
    env_writer("NESSUS_PASS", "What is the password?")
