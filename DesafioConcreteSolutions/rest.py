from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import Column, Integer, String
from DesafioConcreteSolutions import db, app, models
from passlib.hash import sha256_crypt
from datetime import datetime
import jwt
import uuid
import json

users = {}

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
		self.access_token = jwt.encode({ 'payload': email }, 'desafio_concrete_solutions', algorithm='HS256').strip()

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
		return '<Phone (%r) %r>' % (self.ddd, self.number) 

class UsersRestGet(Resource):
	def get(self, user_id):
		return {user_id: users[user_id] if user_id in users else "" }

class UsersRestPost(Resource):
	def post(self):
		# user_id = str(uuid.uuid4())
		for key in request.form.keys():
			new_user = json.loads(key)
			user = User(new_user['name'], new_user['email'], new_user['password'])
			user.phones = []
			for phone in new_user['phones']:
				user.phones.append(Phone(phone['number'], phone['ddd']))
			db.session.add(user)
			db.session.commit()

			return {'id': user.id, 'created': user.created.isoformat(), 'modified': user.modified.isoformat(), 'last_login': user.last_login.isoformat(), 'token': str(user.access_token) }

class UsersRestLogin(Resource):
	def post(self):
		for key in request.form.keys():
			login_data = json.loads(key)
			user = User.query.filter_by(email = login_data['email']).first()
			if user is None:
				return { 'mensagem': 'Usuario e/ou senha invalidos.' }
			if not user.verify_password(login_data['password']):
				return { 'mensagem': 'Usuario e/ou senha invalidos.' }, 401
			return {'id': user.id, 'created': user.created.isoformat(), 'modified': user.modified.isoformat(), 'last_login': user.last_login.isoformat(), 'token': str(user.access_token) }

class UsersRestProfile(Resource):
	def post(self):
		for key in request.form.keys():
			profile_data = json.loads(key)
			user = User.query.filter(User.access_token.like('%' + profile_data['token'] + '%')).first()
			if user is None:
				return { 'mensagem': 'Nao autorizado. (nao encontrado)' }, 401
			if user.id != profile_data['id']:
				return { 'mensagem': 'Nao autorizado. (id incorreto)' }, 401
			if (datetime.now() - user.last_login).total_seconds() > 30 * 60:
				return { 'mensagem': 'Sessao invalida.' }, 401
			user.last_login = datetime.now()
			db.session.commit()
			return {'id': user.id, 'created': user.created.isoformat(), 'modified': user.modified.isoformat(), 'last_login': user.last_login.isoformat(), 'token': str(user.access_token) }
