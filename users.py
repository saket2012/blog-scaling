from flask import Flask, request, jsonify
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
        return False


class Users(Resource):

    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        display_name = data['display_name']
        print(username)
        if username == "" or password == "" or display_name == "":
            response = {'response': "Enter valid details"}
            return jsonify(response)
        email_validator = lepl.apps.rfc3696.Email()
        if not email_validator(username):
            response = {'response': "Enter valid Email"}
            return jsonify(response)
        user_details = users_db.get_user_details(username)
        if user_details:
            response = {'response': "Conflict"}
            return jsonify(response)
        else:
            users_db.create_user(username, password, display_name)
            response = {'response': "Created"}
            return jsonify(response)

    def put(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        new_password = data['new_password']
        if username == "" or password == "" or new_password == "":
            response = {'response': "Enter valid details"}
            return jsonify(response)
        auth = authorization()
        if auth:
            authentication = request.authorization
            if authentication.username == username and authentication.password == password:
                users_db.update_password(username, new_password)
                response = {'response': "OK"}
                return jsonify(response)
            else:
                response = {"Message": "Unauthorized Access"}
                return jsonify(response)
        else:
            response = {"Message": "Could not verify your login!"}
            return jsonify(response)

    def delete(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        if username == "" or password == "" or password == "":
            response = {'response': "Enter valid details"}
            return jsonify(response)
        auth = authorization()
        if auth:
            authentication = request.authorization
            if authentication.username == data['username'] and authentication.password == data['password']:
                users_db.delete_user(data)
                response = {'response': "OK"}
                return jsonify(response)
            else:
                response = {"Message": "Unauthorized Access"}
                return jsonify(response)
        else:
            response = {"Message": "Could not verify your login!"}
            return jsonify(response)


api.add_resource(Users, '/users')

if __name__ == '__main__':
    db_connection.create_tables()
    app.run(debug = True, host = '0.0.0.0', port = 5000)
