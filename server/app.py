#!/usr/bin/env python3

from flask import request, session, make_response
from flask_restful import Resource
from config import app, db, api
from models import User, UserSchema

user_schema = UserSchema()

class Signup(Resource):
    def post(self):
        data = request.get_json()
        try:
            new_user = User(username=data.get('username'))
            new_user.password_hash = data.get('password')

            db.session.add(new_user)
            db.session.commit()

            session['user_id'] = new_user.id
            return user_schema.dump(new_user), 201
        except Exception:
            return {"error": "Could not create user"}, 422

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = User.query.filter(User.id == user_id).first()
            return user_schema.dump(user), 200
        return {}, 204

class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter(User.username == data.get('username')).first()

        if user and user.authenticate(data.get('password')):
            session['user_id'] = user.id
            return user_schema.dump(user), 200
        
        return {"error": "Invalid username or password"}, 401

class Logout(Resource):
    def delete(self):
        if session.get('user_id'):
            session['user_id'] = None
            return {}, 204
        return {"error": "Not logged in"}, 401

class ClearSession(Resource):
    def delete(self):
        session['page_views'] = None
        session['user_id'] = None
        return {}, 204

api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(CheckSession, '/check_session')
api.add_resource(Logout, '/logout')
api.add_resource(ClearSession, '/clear')

if __name__ == '__main__':
    app.run(port=5555, debug=True)