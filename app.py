from flask import Flask, session, flash, redirect, url_for, render_template
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

import os

app = Flask(__name__)
db = SQLAlchemy()
api = Api(app)
mail = Mail(app)


filename = os.path.dirname(os.path.abspath(__file__))
database = "sqlite:///" + os.path.join(filename, "db.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = 'RahasiaKabupatenSukabumi'

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "muhammadanbiya284@gmail.com"
app.config["MAIL_PASSWORD"] = "puguhanpohosandinanaon"
app.config["MAIL_DEFAULT_SENDER"] = "muhammadanbiya284@gmail.com"



db.init_app(app)
mail.init_app(app)


with app.app_context():
    db.create_all()

from routes import *

if __name__ == "__main__":
    app.run(debug=True)
