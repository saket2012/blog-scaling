import json

from flask import Flask, request
from flask_restful import Resource, Api
from passlib.hash import sha256_crypt

import db_connection
import users_db

app = Flask(__name__)
api = Api(app)


class User(Resource):
    def post(self):
        print("in user post")
        data = request.get_json()
        username = data['username']
        password = data['password']
        display_name = data['display_name']
        # Check NULL condition of all fields
        if username == "" or password == "" or display_name == "":
            response = app.response_class(response = json.dumps({"message": "BAD REQUEST"}, indent = 4),
                                          status = 400,
                                          content_type = 'application/json')
            return response
        user_details = users_db.get_user_details(username)
        if user_details:
            # User already exists
            response = app.response_class(response = json.dumps({"message": "CONFLICT"}, indent = 4),
                                          status = 409,
                                          content_type = 'application/json')
            return response
        else:
            # Create a new user
            users_db.create_user(username, password, display_name)
            response = app.response_class(response = json.dumps({"message": "CREATED"}, indent = 4),
                                          status = 201,
                                          content_type = 'application/json')
            return response

    def patch(self):
        print("user update")
        data = request.get_json()
        username = request.authorization.username
        new_password = data['new_password']
        # Check NULL condition of all fields
        if new_password == "":
            response = app.response_class(response = json.dumps({"message": "BAD REQUEST"}, indent = 4),
                                          status = 400,
                                          content_type = 'application/json')
            return response
        users_db.update_password(username, new_password)
        response = app.response_class(response = json.dumps({"message": "OK"}, indent = 4),
                                      status = 200,
                                      content_type = 'application/json')
        return response

    def delete(self):
        print("user delete")
        username = request.authorization.username
        users_db.delete_user(username)
        response = app.response_class(response = json.dumps({"message": "OK"}, indent = 4),
                                      status = 200,
                                      content_type = 'application/json')
        return response


class Authentication(Resource):
    def get(self):
        username = request.authorization.username
        password = request.authorization.password
        passwd = users_db.get_user_details(username)
        if passwd:
            passwd = passwd[0]
            passwd = passwd[2]
            if sha256_crypt.verify(password, passwd):
                response = app.response_class(response = json.dumps({"message": "OK"}, indent = 4),
                                              status = 200,
                                              content_type = 'application/json')
                return response
            else:
                response = app.response_class(response = json.dumps({"message": "UNAUTHORIZED"}, indent = 4),
                                              status = 401,
                                              content_type = 'application/json')
                return response
        else:
            response = app.response_class(response = json.dumps({"message": "UNAUTHORIZED"}, indent = 4),
                                          status = 401,
                                          content_type = 'application/json')
            return response


api.add_resource(User, '/user')
api.add_resource(Authentication, '/authenticate')


if __name__ == '__main__':
    db_connection.create_tables()
    app.run(debug = True, host = '0.0.0.0')
