"""
The flask application package.
"""

from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\sqlite\\test.db'
db = SQLAlchemy(app)
db.init_app(app)
db.create_all()
api = Api(app)

import DesafioConcreteSolutions.views
import DesafioConcreteSolutions.rest
