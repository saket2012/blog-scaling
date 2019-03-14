from flask import Flask, request, jsonify, Response
import users_db, db_connection
import lepl.apps.rfc3696
from flask_restful import Resource, Api

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
            response = Response(status = 400, mimetype = 'application/json')
            return response
        email_validator = lepl.apps.rfc3696.Email()
        if not email_validator(username):
            # Email validation
            response = Response(status = 400, mimetype = 'application/json')
            return response
        user_details = users_db.get_user_details(username)
        if user_details:
            #User already exists
            response = Response(status = 409, mimetype = 'application/json')
            return response
        else:
            # Create a new user
            users_db.create_user(username, password, display_name)
            response = Response(status = 201, mimetype = 'application/json')
            return response

    def patch(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        new_password = data['new_password']
        # Check NULL condition of all fields
        if username == "" or password == "" or new_password == "":
            response = Response(status = 400, mimetype = 'application/json')
            return response
        auth = authorization()
        # Check authentication
        if auth is not None:
            if auth:
                authentication = request.authorization
                if authentication.username == username and authentication.password == password:
                    users_db.update_password(username, new_password)
                    response = Response(status = 200, mimetype = 'application/json')
                    return response
                else:
                    # Unauthorized access
                    response = Response(status = 401, mimetype = 'application/json')
                    return response
            else:
                # Unauthorized access
                response = Response(status = 401, mimetype = 'application/json')
                return response
        else:
            # User not found
            response = Response(status = 404, mimetype = 'application/json')
            return response

    def delete(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        # Check NULL condition of all fields
        if username == "" or password == "" or password == "":
            response = Response(status = 400, mimetype = 'application/json')
            return response
        auth = authorization()
        # Check authentication
        if auth is not None:
            if auth:
                authentication = request.authorization
                if authentication.username == data['username'] and authentication.password == data['password']:
                    # Delete a user
                    users_db.delete_user(data)
                    response = Response(status = 200, mimetype = 'application/json')
                    return response
                else:
                    # Unauthorized access
                    response = Response(status = 401, mimetype = 'application/json')
                    return response
            else:
                # Unauthorized access
                response = Response(status = 401, mimetype = 'application/json')
                return response
        else:
            # User not found
            response = Response(status = 404, mimetype = 'application/json')
            return response


api.add_resource(Users, '/users')

if __name__ == '__main__':
    db_connection.create_tables()
    app.run(debug = True, host = '0.0.0.0', port = 5000)
