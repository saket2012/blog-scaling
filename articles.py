from flask import Flask, request, jsonify, Response, make_response
import users_db, db_connection, articles_db
import json
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# HTTP Authentication
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


class Articles(Resource):

    # Post new article
    def post(self):
        data = request.get_json()
        text = data['text']
        author = data['author']
        title = data['title']
        url = data['url']
        # Check NULL condition of all fields
        if text == "" or author == "" or title == "" or url == "":
            response = app.response_class(response = json.dumps({"message": "Bad Request"}, indent = 4),
                                          status = 400,
                                          content_type = 'application/json')
            return response
        auth = authorization()
        # Check authentication
        if auth is not None:
            if auth:
                authentication = request.authorization
                user_id = users_db.get_user_details(authentication.username)
                user_id = user_id[0]
                # Post an article
                articles_db.post_article(user_id[0], text, author, title, url)
                # Get article id
                article_id = articles_db.get_article(title)
                article_id = article_id[0]
                response = Response("article is created",status = 201, mimetype = 'application/json')
                response.headers['location'] = 'http://127.0.0.1:5000/articles/' + str(article_id[0])
                response.body = 'Article' + title + 'is added'
                return response
            else:
                # Unauthorized access
                response = app.response_class(response = json.dumps({"message": "Conflict"}, indent = 4),
                                              status = 401,
                                              content_type = 'application/json')
                return response
        else:
            # User not found
            response = app.response_class(response = json.dumps({"message": "Not Found"}, indent = 4),
                                          status = 404,
                                          content_type = 'application/json')
            return response

    # Update an article
    def put(self):
        data = request.get_json()
        title = data['title']
        author = data['author']
        text = data['text']
        # Check NULL condition of all fields
        if text == "" or author == "" or title == "" or text == "":
            response = app.response_class(response = json.dumps({"message": "Bad Request"}, indent = 4),
                                          status = 400,
                                          content_type = 'application/json')
            return response
        auth = authorization()
        # Check authentication
        if auth is not None:
            if auth:
                authentication = request.authorization
                user_details = users_db.get_user_details(authentication.username)
                user_details = user_details[0]
                article_id = articles_db.get_article_details(user_details[0], title)
                if not article_id:
                    # Check if article exists or not
                    response = app.response_class(response = json.dumps({"message": "Not Found"}, indent = 4),
                                                  status = 404,
                                                  content_type = 'application/json')
                    return response
                article_id = article_id[0]
                article_user_id = article_id[1]
                # Allow editing of an article posted by the same user
                if article_user_id == user_details[0]:
                    # Edit article
                    articles_db.edit_article(title, author, text, article_id[0])
                    response = app.response_class(response = json.dumps({"message": "OK"}, indent = 4),
                                                  status = 200,
                                                  content_type = 'application/json')
                    return response
                else:
                    # Unauthorized access
                    response = app.response_class(response = json.dumps({"message": "Conflict"}, indent = 4),
                                                  status = 409,
                                                  content_type = 'application/json')
                    return response
            else:
                # Unauthorized access
                response = app.response_class(response = json.dumps({"message": "Conflict"}, indent = 4),
                                              status = 409,
                                              content_type = 'application/json')
                return response
        else:
            # User not found
            response = app.response_class(response = json.dumps({"message": "Not Found"}, indent = 4),
                                          status = 404,
                                          content_type = 'application/json')
            return response

    # Delete an article
    def delete(self):
        data = request.get_json()
        title = data['title']
        # Check NULL condition of all fields
        if title == "":
            response = app.response_class(response = json.dumps({"message": "Bad Request"}, indent = 4),
                                          status = 400,
                                          content_type = 'application/json')
            return response
        auth = authorization()
        # Check Authentication
        if auth is not None:
            if auth:
                authentication = request.authorization
                user_details = users_db.get_user_details(authentication.username)
                user_details = user_details[0]
                article_id = articles_db.get_article_details(user_details[0], title)
                if not article_id:
                    # Article not found
                    response = app.response_class(response = json.dumps("Articles Not Found", indent = 4),
                                                  status = 404,
                                                  content_type = 'application/json')
                    return response
                article_id = article_id[0]
                article_user_id = article_id[1]
                if article_user_id == user_details[0]:
                    # Delete an article
                    articles_db.delete_article(article_id[0])
                    response = app.response_class(response = json.dumps({"message": "OK"}, indent = 4),
                                                  status = 200,
                                                  content_type = 'application/json')
                    return response
                else:
                    # Unauthorized access
                    response = app.response_class(response = json.dumps({"message": "Conflict"}, indent = 4),
                                                  status = 409,
                                                  content_type = 'application/json')
                    return response
            else:
                # Unauthorized access
                response = app.response_class(response = json.dumps({"message": "Conflict"}, indent = 4),
                                              status = 409,
                                              content_type = 'application/json')
                return response
        else:
            # User not found
            response = app.response_class(response = json.dumps("User Not Found", indent = 4),
                                          status = 404,
                                          content_type = 'application/json')
            return response

    def get(self):
        data = request.get_json()
        title = data['title']
        # Check NULL condition of all fields
        if title == "":
            response = app.response_class(response = json.dumps("Articles Not Found", indent = 4),
                                          status = 404,
                                          content_type = 'application/json')
            return response
        article = articles_db.get_article(title)
        if not article:
            # Article not found
            message = {'message':'Article not found'}
            return jsonify(message)
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

class N_Articles(Resource):
    def get(self, no_of_articles):
        n_articles = articles_db.get_n_articles(no_of_articles)
        if not n_articles:
            response = app.response_class(response = json.dumps("Articles Not Found",indent = 4),
                                          status = 404,
                                          content_type = 'application/json')
            return response
        response = app.response_class(response = json.dumps(n_articles, indent = 4),
                                      status = 200,
                                      content_type = 'application/json')
        return response


class Article_Metadata(Resource):
    def get(self, no_of_articles):
        n_articles = articles_db.get_articles_metadata(no_of_articles)
        if not n_articles:
            response = app.response_class(response = json.dumps("Articles Not Found",indent = 4),
                                          status = 404,
                                          content_type = 'application/json')
            return response
        response = app.response_class(response = json.dumps(n_articles, indent = 4),
                                      status = 200,
                                      content_type = 'application/json')
        return response



api.add_resource(Articles, '/articles') # Route 1
api.add_resource(N_Articles, '/articles/<no_of_articles>') # Route 2
api.add_resource(Article_Metadata, '/articles_metadata/<no_of_articles>') # Route 2


if __name__ == '__main__':
    db_connection.create_tables()
    app.run(debug = True, host = '0.0.0.0', port = 5001)
