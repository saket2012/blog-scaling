from flask import Flask, request, jsonify, Response
import users_db, db_connection
from flask_restful import Resource, Api
import json
from flask_httpauth import HTTPBasicAuth
from passlib.hash import sha256_crypt



app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

@auth.verify_password
def verify(username, password):
    passwd = users_db.get_user_details(username)
    if passwd:
        passwd = passwd[0]
        passwd = passwd[2]
        if sha256_crypt.verify(password, passwd):
            return True
        else:
            return False
    else:
        return False


class Users(Resource):

    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        display_name = data['display_name']
        # Check NULL condition of all fields
        if username == "" or password == "" or display_name == "":
            response = app.response_class(response = json.dumps({"message":"Bad Request"}, indent = 4),
                                          status = 400,
                                          content_type = 'application/json')
            return response
        user_details = users_db.get_user_details(username)
        if user_details:
            #User already exists
            response = app.response_class(response = json.dumps({"message":"Conflict"}, indent = 4),
                                          status = 409,
                                          content_type = 'application/json')
            return response
        else:
            # Create a new user
            users_db.create_user(username, password, display_name)
            response = app.response_class(response = json.dumps({"message": "Created"}, indent = 4),
                                          status = 201,
                                          content_type = 'application/json')
            return response

    @auth.login_required
    def patch(self):
        data = request.get_json()
        username = request.authorization.username
        new_password = data['new_password']
        # Check NULL condition of all fields
        if new_password == "":
            response = app.response_class(response = json.dumps({"message": "Bad Request"}, indent = 4),
                                          status = 400,
                                          content_type = 'application/json')
            return response
        users_db.update_password(username, new_password)
        response = app.response_class(response = json.dumps({"message": "OK"}, indent = 4),
                                                  status = 200,
                                                  content_type = 'application/json')
        return response

    @auth.login_required
    def delete(self):
        username = request.authorization.username
        users_db.delete_user(username)
        response = app.response_class(response = json.dumps({"message": "OK"}, indent = 4),
                                                  status = 200,
                                                  content_type = 'application/json')
        return response

api.add_resource(Users, '/users')

if __name__ == '__main__':
    db_connection.create_tables()
    app.run(debug = True, host = '0.0.0.0')
