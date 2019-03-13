from flask import Flask, request, jsonify
import users_db, db_connection, articles_db
import json

app = Flask(__name__)


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


@app.route('/article/post', methods = ['POST'])
def post_article():
    data = request.get_json()
    auth = authorization()
    if auth:
        authentication = request.authorization
        user_id = users_db.get_user_details(authentication.username)
        user_id = user_id[0]
        articles_db.post_article(user_id[0], data)
        return jsonify({"Message": "Created"}), 201
    else:
        return jsonify({"Message": "Could not verify your login!"}), 401


@app.route('/article/edit', methods = ['PUT'])
def edit_article():
    data = request.get_json()
    auth = authorization()
    if auth:
        authentication = request.authorization
        user_details = users_db.get_user_details(authentication.username)
        user_details = user_details[0]
        article_id = articles_db.get_article_details(user_details[0], data)
        if not article_id:
            return jsonify({"Message": "Not Found"}), 404
        article_id = article_id[0]
        article_user_id = article_id[1]
        if article_user_id == user_details[0]:
            articles_db.edit_article(data, article_id[0])
            return jsonify({"Message": "OK"}), 200
        else:
            return jsonify({"Message": "Unauthorized Access"}), 401
    else:
        return jsonify({"Message": "Could not verify your login!"}), 401


@app.route('/article/delete', methods = ['DELETE'])
def delete_article():
    data = request.get_json()
    auth = authorization()
    if auth:
        authentication = request.authorization
        user_details = users_db.get_user_details(authentication.username)
        user_details = user_details[0]
        article_id = articles_db.get_article_details(user_details[0], data)
        if not article_id:
            return jsonify({"Message": "Not Found"}), 404
        article_id = article_id[0]
        article_user_id = article_id[1]
        if article_user_id == user_details[0]:
            articles_db.delete_article(article_id[0])
            return jsonify({"Message": "OK"}), 200
        else:
            return jsonify({"Message": "Unauthorized Access"}), 401
    else:
        return jsonify({"Message": "Could not verify your login!"}), 401


@app.route('/article/retrieve')
def get_article():
    data = request.get_json()
    title = data['title']
    article = articles_db.get_article(title)
    if not article:
        return jsonify({"Message": "Not Found"}), 404
    article = article[0]
    title = article[4]
    author = article[3]
    text = article[2]
    return jsonify({"Title": title,
                    "Author": author,
                    "Text": text})


@app.route('/article/retrieve_n_most')
def retrieve_n_most():
    data = request.get_json()
    n = data['no_of_articles']
    n_articles = articles_db.get_n_articles(n)
    with open('articles.txt', 'w') as article:
        json.dump(n_articles, article, indent = 4)
    return jsonify({"Message": "OK"}), 200


@app.route('/article/retrieve_metadata')
def retrieve_metadata():
    data = request.get_json()
    n = data['no_of_articles']
    n_articles = articles_db.get_articles_metadata(n)
    with open('articles_metadata.txt', 'w') as article:
        json.dump(n_articles, article, indent = 4)
    return jsonify({"Message": "OK"}), 200


if __name__ == '__main__':
    db_connection.create_tables()
    app.run(debug = True, host = '0.0.0.0', port = 5001)
