from flask import Flask, render_template, request, redirect, session
import os

# Importing the necessary modules and libraries
from flask import Flask
from flask_migrate import Migrate
from routes.blueprint import blueprint

STATIC_DIR = os.path.abspath('static')

def create_app():
    app = Flask(__name__)  # flask app object
    app.config.from_object('config')  # Configuring from Python Files
    app = Flask(__name__, static_folder=STATIC_DIR)
    app.use_static_for_root = True
    app.secret_key = 'HI'
    return app

app = create_app()  # Creating the app
# Registering the blueprint
app.register_blueprint(blueprint, url_prefix='')

if __name__ == '__main__':  # Running the app
    app.run(host='127.0.0.1', port=5000, debug=True)