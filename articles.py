import json

from flask import Flask, request, Response
from flask_restful import Resource, Api

import articles_db
import db_connection

app = Flask(__name__)
api = Api(app)


class Articles(Resource):
    # Post new article
    def post(self):
        data = request.get_json()
        text = data['text']
        author = data['author']
        title = data['title']
        url = data['url']
        username = request.authorization.username
        # Check NULL condition of all fields
        if text == "" or author == "" or title == "" or url == "":
            response = app.response_class(response = json.dumps({"message": "BAD REQUEST"}, indent = 4),
                                          status = 400,
                                          content_type = 'application/json')
            return response
        # Post an article
        articles_db.post_article(username, text, author, title, url)
        # Get article id
        article_id = articles_db.get_article(title)
        article_id = article_id[0]
        response = Response("article is created",status = 201, mimetype = 'application/json')
        response.headers['location'] = "http://127.0.0.1:5100/articles/" + str(article_id[5])
        return response

    # Update an article
    def put(self):
        data = request.get_json()
        title = data['title']
        author = data['author']
        text = data['text']
        username = request.authorization.username
        # Check NULL condition of all fields
        if text == "" or author == "" or title == "" or text == "":
            response = app.response_class(response = json.dumps({"message": "BAD REQUEST"}, indent = 4),
                                          status = 400,
                                          content_type = 'application/json')
            return response
        article_id = articles_db.get_article_details(username, title)
        if not article_id:
            # Check if article exists or not
            response = app.response_class(response = json.dumps({"message": "NOT FOUND"}, indent = 4),
                                          status = 404,
                                          content_type = 'application/json')
            return response
        article_id = article_id[0]
        articles_db.edit_article(author, text, article_id[0])
        response = app.response_class(response = json.dumps({"message": "OK"}, indent = 4),
                                      status = 200,
                                      content_type = 'application/json')
        return response

    # Delete an article
    def delete(self):
        data = request.get_json()
        title = data['title']
        username = request.authorization.username
        # Check NULL condition of all fields
        if title == "":
            response = app.response_class(response = json.dumps({"message": "BAD REQUEST"}, indent = 4),
                                          status = 400,
                                          content_type = 'application/json')
            return response
        article_id = articles_db.get_article_details(username, title)
        if not article_id:
            # Article not found
            response = app.response_class(response = json.dumps({"message": "NOT FOUND"}, indent = 4),
                                          status = 404,
                                          content_type = 'application/json')
            return response
        article_id = article_id[0]
        # Delete an article
        articles_db.delete_article(article_id[0])
        response = app.response_class(response = json.dumps({"message": "OK"}, indent = 4),
                                      status = 200,
                                      content_type = 'application/json')
        return response

    def get(self):
        data = request.get_json()
        title = data['title']
        # Check NULL condition of all fields
        if title == "":
            response = app.response_class(response = json.dumps({"message": "BAD REQUEST"}, indent = 4),
                                          status = 400,
                                          content_type = 'application/json')
            return response
        article = articles_db.get_article(title)
        if not article:
            # Article not found
            response = app.response_class(response = json.dumps({"message": "NOT FOUND"}, indent = 4),
                                          status = 404,
                                          content_type = 'application/json')
            return response
        article = article[0]
        title = article[4]
        author = article[3]
        text = article[2]
        message = {'Title': title,
                   'Author': author,
                   'Text': text}
        response = app.response_class(response = json.dumps(message, indent = 4),
                                      status = 200,
                                      content_type = 'application/json')
        return response


class NArticles(Resource):
    def get(self):
        data = request.get_json()
        no_of_articles = data['no_of_articles']
        n_articles = articles_db.get_n_articles(no_of_articles)
        if not n_articles:
            response = app.response_class(response = json.dumps({"message": "NOT FOUND"}, indent = 4),
                                          status = 404,
                                          content_type = 'application/json')
            return response
        response = app.response_class(response = json.dumps(n_articles, indent = 4),
                                      status = 200,
                                      content_type = 'application/json')
        return response


class ArticleMetadata(Resource):
    def get(self, no_of_articles):
        # data = request.get_json()
        # no_of_articles = data['no_of_articles']
        n_articles = articles_db.get_articles_metadata(no_of_articles)
        if not n_articles:
            response = app.response_class(response = json.dumps({"message": "NOT FOUND"}, indent = 4),
                                          status = 404,
                                          content_type = 'application/json')
            return response
        response = app.response_class(response = json.dumps(n_articles, indent = 4),
                                      status = 200,
                                      content_type = 'application/json')
        return response


api.add_resource(Articles, '/article')  # Route 1
api.add_resource(NArticles, '/articles-data')  # Route 2
api.add_resource(ArticleMetadata, '/articles-metadata/<no_of_articles>')  # Route 3


if __name__ == '__main__':
    db_connection.create_tables()
    app.run(debug = True, host = '0.0.0.0', port = 5100)
