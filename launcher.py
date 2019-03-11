from flask import Flask, request, make_response, jsonify
import user, db_connection, articles
import json

app = Flask(__name__)


def authorization():
    auth = request.authorization
    user_details = user.get_user_details(auth.username)
    if user_details:
        user_details = user_details[0]
        password = user.encode_password(auth.password)
        auth = request.authorization
        if auth and auth.username == user_details[1] and user_details[2] == password:
            return True
        else:
            return False
    else:
        return False


@app.route('/users/register', methods = ['POST'])
def create_user():
    data = request.get_json()
    username = data['username']
    user_details = user.get_user_details(username)
    print(user_details)
    if user_details:
        return jsonify({"Message": "User already exists"}), 401
    else:
        user.create_user(data)
        return jsonify({"Message": "New user is created successfully"}), 200


@app.route('/users/update', methods = ['POST'])
def update_password():
    data = request.get_json()
    auth = authorization()
    if auth:
        authentication = request.authorization
        if authentication.username == data['username']:
            user.update_password(data)
            return jsonify({"Message": "Password is updated successfully"}), 200
        else:
            return jsonify({"Message": "Username does not match"}), 409
    else:
        return make_response('Could not verify your login!', 401, {
            'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route('/users/delete_user', methods = ['POST'])
def delete_user():
    data = request.get_json()
    auth = authorization()
    if auth:
        authentication = request.authorization
        if authentication.username == data['username']:
            user.delete_user(data)
            return jsonify({"Message": "User is deleted successfully"}), 200
        else:
            return jsonify({"Message": "Username does not match"}), 409

    else:
        return make_response('Could not verify your login!', 401, {
            'WWW-Authenticate': 'Basic realm="Login Required"'})
    

@app.route('/article/post', methods = ['POST'])
def post_article():
    data = request.get_json()
    articles.post_article(data)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    db_connection.create_tables()
    app.run(debug = True)
