from flask import Flask, request, jsonify
import user, db_connection, articles
import lepl.apps.rfc3696

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


@app.route('/users/register_user', methods = ['POST'])
def create_user():
    data = request.get_json()
    username = data['username']
    email_validator = lepl.apps.rfc3696.Email()
    if not email_validator(username):
        return jsonify({"Message": "Enter valid details"}), 401
    user_details = user.get_user_details(username)
    if user_details:
        return jsonify({"Message": "User already exists"}), 409
    else:
        user.create_user(data)
        return jsonify({"Message": "New user is created successfully"}), 200


@app.route('/users/update_user', methods = ['POST'])
def update_password():
    data = request.get_json()
    auth = authorization()
    if auth:
        authentication = request.authorization
        if authentication.username == data['username'] and authentication.password == data['password']:
            user.update_password(data)
            return jsonify({"Message": "Password is updated successfully"}), 200
        else:
            return jsonify({"Message": "Username or password does not match"}), 409
    else:
        return jsonify({"Message": "Could not verify your login!"}), 401


@app.route('/users/delete_user', methods = ['POST'])
def delete_user():
    data = request.get_json()
    auth = authorization()
    if auth:
        authentication = request.authorization
        if authentication.username == data['username'] and authentication.password == data['password']:
            user.delete_user(data)
            return jsonify({"Message": "User is deleted successfully"}), 200
        else:
            return jsonify({"Message": "Username or password does not match"}), 409
    else:
        return jsonify({"Message": "Could not verify your login!"}), 401


@app.route('/article/post', methods = ['POST'])
def post_article():
    data = request.get_json()
    auth = authorization()
    if auth:
        authentication = request.authorization
        user_id = user.get_user_details(authentication.username)
        user_id = user_id[0]
        articles.post_article(user_id[0], data)
        return jsonify({"Message": "Article is posted successfully"}), 200


@app.route('/article/edit', methods = ['POST'])
def edit_article():
    data = request.get_json()
    auth = authorization()
    if auth:
        authentication = request.authorization
        user_details = user.get_user_details(authentication.username)
        user_details = user_details[0]
        article_id = articles.get_article_details(user_details[0], data)
        if not article_id:
            return jsonify({"Message": "Article does not found"}), 401
        article_id = article_id[0]
        article_user_id = article_id[1]
        if article_user_id == user_details[0]:
            articles.edit_article(data, article_id[0])
            return jsonify({"Message": "Article is updated successfully"}), 200
        else:
            return jsonify({"Message": "You can only update articles posted by you"}), 401
    else:
        return jsonify({"Message": "Could not verify your login!"}), 401


@app.route('/article/delete', methods = ['POST'])
def delete_article():
    data = request.get_json()
    auth = authorization()
    if auth:
        authentication = request.authorization
        user_details = user.get_user_details(authentication.username)
        user_details = user_details[0]
        article_id = articles.get_article_details(user_details[0], data)
        if not article_id:
            return jsonify({"Message": "Article does not found"}), 401
        article_id = article_id[0]
        article_user_id = article_id[1]
        if article_user_id == user_details[0]:
            articles.delete_article(article_id[0])
            return jsonify({"Message": "Article is deleted successfully"}), 200
        else:
            return jsonify({"Message": "You can only delete articles posted by you"}), 401
    else:
        return jsonify({"Message": "Could not verify your login!"}), 401


@app.route('/article/retrieve', methods = ['POST'])
def retrieve_article():
    data = request.get_json()
    title = data['title']
    article = articles.get_article(title)
    if not article:
        return jsonify({"Message": "Article does not found"}), 401
    article = article[0]
    title = article[4]
    author = article[3]
    text = article[2]
    return jsonify({"Title": title,
                    "Author": author,
                    "Article": text})


if __name__ == '__main__':
    db_connection.create_tables()
    app.run(debug = True)
