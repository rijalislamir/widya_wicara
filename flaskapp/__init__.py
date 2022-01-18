from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://bcyibotyscmphi:630df1b531c1f7fdce1d59ff43ce27d84a5339bac3f6849070175856707b4ed3@ec2-3-222-49-168.compute-1.amazonaws.com:5432/daitfpr32kdg57'
db = SQLAlchemy(app)
ma = Marshmallow(app)

from flaskapp import routes
