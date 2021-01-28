"""Example of a one file Flask application that uses and API and ORM"""

import requests  # allows us to make request to the API
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Configurations for application

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


DB = SQLAlchemy(app)


# Routes for application

@app.route("/")
def root():
    astro_data = Astronauts.query.all()[0]
    return "{}".format(astro_data)


@app.route("/refresh")
def refresh():
    DB.drop_all()
    DB.create_all()
    api_request = requests.get("http://api.open-notify.org/astros.json")
    astro_data = api_request.json()
    num_astros = astro_data["number"]
    # Save to SQL DB
    record = Astronauts(num_astronauts=num_astros)
    DB.session.add(record)
    DB.session.commit()
    return "Database Updated!"


@app.route("/iss-location")
def iss():
    api_request = requests.get("http://api.open-notify.org/iss-now.json")
    iss_location = api_request.json()
    position = iss_location["iss_position"]
    return "The ISS is here: (LO: {}, LA: {})".format(position["longitude"], position["latitude"])


# Database tables using SQLAlchemy
class Astronauts(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    num_astronauts = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return "# of astros: {}".format(self.num_astronauts)
