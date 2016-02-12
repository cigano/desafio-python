'''from sqlalchemy import Column, Integer, String
from DesafioConcreteSolutions import db
from passlib.hash import sha256_crypt
from datetime import datetime
import jwt

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), unique=True)
	email = db.Column(db.String(200), unique=True)
	password = db.Column(db.String(200))
	created = db.Column(db.DateTime)
	modified = db.Column(db.DateTime)
	last_login = db.Column(db.DateTime)
	access_token = db.Column(db.String(200), unique=True)
	phones = db.relationship('Phone', backref='user',
                                lazy='dynamic')	

	def __init__(self, name, email, password):
		self.name = name
		self.email = email
		self.password = sha256_crypt.encrypt(password)
		now = datetime.now()
		self.created = now
		self.modified = now
		self.last_login = now
		self.access_token = jwt.encode({ 'payload': email }, 'desafio_concrete_solutions', algorithm='HS256')

	def __repr__(self):
		return '<User %r>' % self.name

	def verify_password(self, attempted_password):
		return sha256_crypt.verify(attempted_password, self.password)

class Phone(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	number = db.Column(db.String(9))
	ddd = db.Column(db.String(2))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __init__(self, number, ddd):
		self.number = number
		self.ddd = ddd

	def __repr__(self):
		return '<Phone (%r) %r>' % (self.ddd, self.number) '''