from flask import Flask, request, jsonify, Response
import users_db, db_connection
from flask_restful import Resource, Api
import json

app = Flask(__name__)
api = Api(app)


def authorization():
    auth = request.authorization
    user_details = users_db.get_user_details(auth.username)
    if user_details:
        user_details = user_details[0]
        password = users_db.encode_password(auth.password)
        auth = request.authorization
        if auth and auth.username == user_details[1] and user_details[2] == password:
            return True
        else:
            return False
    else:
        return None


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

    def patch(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        new_password = data['new_password']
        # Check NULL condition of all fields
        if username == "" or password == "" or new_password == "":
            response = app.response_class(response = json.dumps({"message": "Bad Request"}, indent = 4),
                                          status = 400,
                                          content_type = 'application/json')
            return response
        auth = authorization()
        # Check authentication
        if auth is not None:
            if auth:
                authentication = request.authorization
                if authentication.username == username and authentication.password == password:
                    users_db.update_password(username, new_password)
                    response = app.response_class(response = json.dumps({"message": "OK"}, indent = 4),
                                                  status = 200,
                                                  content_type = 'application/json')
                    return response
                else:
                    # Unauthorized access
                    response = app.response_class(response = json.dumps({"message": "Unauthorized"}, indent = 4),
                                                  status = 401,
                                                  content_type = 'application/json')
                    return response
            else:
                # Unauthorized access
                response = app.response_class(response = json.dumps({"message": "Unauthorized"}, indent = 4),
                                              status = 401,
                                              content_type = 'application/json')
                return response
        else:
            # User not found
            response = app.response_class(response = json.dumps({"message": "Not Found"}, indent = 4),
                                          status = 404,
                                          content_type = 'application/json')
            return response

    def delete(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        # Check NULL condition of all fields
        if username == "" or password == "" or password == "":
            response = app.response_class(response = json.dumps({"message": "Bad Request"}, indent = 4),
                                          status = 400,
                                          content_type = 'application/json')
            return response
        auth = authorization()
        # Check authentication
        if auth is not None:
            if auth:
                authentication = request.authorization
                if authentication.username == data['username'] and authentication.password == data['password']:
                    # Delete a user
                    users_db.delete_user(data)
                    response = app.response_class(response = json.dumps({"message": "OK"}, indent = 4),
                                                  status = 200,
                                                  content_type = 'application/json')
                    return response
                else:
                    # Unauthorized access
                    response = app.response_class(response = json.dumps({"message": "Unauthorized"}, indent = 4),
                                                  status = 401,
                                                  content_type = 'application/json')
                    return response
            else:
                # Unauthorized access
                response = app.response_class(response = json.dumps({"message": "Unauthorized"}, indent = 4),
                                              status = 401,
                                              content_type = 'application/json')
                return response
        else:
            # User not found
            response = app.response_class(response = json.dumps({"message": "Not Found"}, indent = 4),
                                          status = 404,
                                          content_type = 'application/json')
            return response


api.add_resource(Users, '/users')

if __name__ == '__main__':
    db_connection.create_tables()
    app.run(debug = True, host = '0.0.0.0')
