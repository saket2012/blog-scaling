from flask import Flask, request, jsonify
import users_db, db_connection, articles_db
import json
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


class Articles(Resource):

    def post(self):
        data = request.get_json()
        text = data['text']
        author = data['author']
        title = data['title']
        url = data['url']
        if text == "" or author == "" or title == "" or url == "":
            response = {'response': "Enter valid details"}
            return jsonify(response)
        auth = authorization()
        if auth:
            authentication = request.authorization
            user_id = users_db.get_user_details(authentication.username)
            user_id = user_id[0]
            articles_db.post_article(user_id[0], text, author, title, url)
            response = {'response': "Created"}
            return jsonify(response)
        else:
            response = {"Message": "Could not verify your login!"}
            return jsonify(response)

    def put(self):
        data = request.get_json()
        title = data['title']
        author = data['author']
        text = data['text']
        if text == "" or author == "" or title == "" or text == "":
            response = {'response': "Enter valid details"}
            return jsonify(response)
        auth = authorization()
        if auth:
            authentication = request.authorization
            user_details = users_db.get_user_details(authentication.username)
            user_details = user_details[0]
            article_id = articles_db.get_article_details(user_details[0], title)
            if not article_id:
                response = {'response': "Not Found"}
                return jsonify(response)
            article_id = article_id[0]
            article_user_id = article_id[1]
            if article_user_id == user_details[0]:
                articles_db.edit_article(title, author, text, article_id[0])
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
        title = data['title']
        if title == "":
            response = {'response': "Enter valid details"}
            return jsonify(response)
        auth = authorization()
        if auth:
            authentication = request.authorization
            user_details = users_db.get_user_details(authentication.username)
            user_details = user_details[0]
            article_id = articles_db.get_article_details(user_details[0], title)
            if not article_id:
                response = {'response': "Not Found"}
                return jsonify(response)
            article_id = article_id[0]
            article_user_id = article_id[1]
            if article_user_id == user_details[0]:
                articles_db.delete_article(article_id[0])
                response = {'response': "OK"}
                return jsonify(response)
            else:
                response = {"Message": "Unauthorized Access"}
                return jsonify(response)
        else:
            response = {"Message": "Could not verify your login!"}
            return jsonify(response)

    def get(self):
        data = request.get_json()
        title = data['title']
        if title == "":
            response = {'response': "Enter valid details"}
            return jsonify(response)
        article = articles_db.get_article(title)
        article = article[0]
        if not article:
            response = {'response': "Not Found"}
            return jsonify(response)
        title = article[4]
        author = article[3]
        text = article[2]
        response = {"Title": title,
                    "Author": author,
                    "Text": text}
        return jsonify(response)


class N_Articles(Resource):
    def get(self, no_of_articles):
        n_articles = articles_db.get_n_articles(no_of_articles)
        if not n_articles:
            response = {'response': "Not Found"}
            return jsonify(response)
        with open('articles.txt', 'w') as article:
            json.dump(n_articles, article, indent = 4)
        response = {'response': "OK"}
        return jsonify(response)


api.add_resource(Articles, '/articles')
api.add_resource(N_Articles, '/articles/<no_of_articles>')

# @app.route('/article/retrieve_metadata')
# def retrieve_metadata():
#     data = request.get_json()
#     n = data['no_of_articles']
#     n_articles = articles_db.get_articles_metadata(n)
#     with open('articles_metadata.txt', 'w') as article:
#         json.dump(n_articles, article, indent = 4)
#     return jsonify({"Message": "OK"}), 200


if __name__ == '__main__':
    db_connection.create_tables()
    app.run(debug = True, host = '0.0.0.0', port = 5001)
