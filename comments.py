import json

from flask import request, Flask
from flask_restful import Api, Resource

import articles_db
import comments_db
import db_connection

app = Flask(__name__)
api = Api(app)

class Comments(Resource):

    def post(self):
        data = request.get_json()
        comment = data['comment']
        article_name = data['article_name']
        username = request.authorization.username
        article_id = articles_db.get_article(article_name)
        if article_id:
            comments_db.post_comment(username, article_name, comment)
            response = app.response_class(response = json.dumps({"message": "CREATED"}, indent = 4),
                                          status = 201,
                                          content_type = 'application/json')
            return response
        else:
            response = app.response_class(response = json.dumps({"message": "NOT FOUND"}, indent = 4),
                                          status = 404,
                                          content_type = 'application/json')
            return response

    def delete(self):
        # Delete an individual comment
        data = request.get_json()
        comment_id = data['comment_id']
        comment = comments_db.get_comment(comment_id)
        if comment:
            comments_db.delete_comment(comment_id)
            response = app.response_class(response=json.dumps({"message": "OK"}, indent=4),
                                          status=200,
                                          content_type='application/json')
            return response
        else:
            response = app.response_class(response = json.dumps({"message": "NOT FOUND"}, indent = 4),
                                          status=404,
                                          content_type='application/json')
            return response

    def get(self):
        # Retrieve the number of comments on a given article
        data = request.get_json()
        article_name = data['article_name']
        n_comments = comments_db.count_comments(article_name)
        if n_comments > 0:
            no_of_comments = {'No of comments': n_comments}
            response = app.response_class(response = json.dumps(no_of_comments, indent = 4),
                                          status = 200,
                                          content_type = 'application/json')
            return response
        else:
            response = app.response_class(response = json.dumps({"message": "NOT FOUND"}, indent = 4),
                                          status = 404,
                                          content_type = 'application/json')
            return response


class NComments(Resource):
    def get(self):
        # Retrieve the n most recent comments on a URL
        data = request.get_json()
        article_name = data['article_name']
        no_of_comments = data['no_of_comments']
        comments = comments_db.get_comments(article_name, no_of_comments)
        if comments:
            response = app.response_class(response = json.dumps(comments, indent = 4),
                                          status = 404,
                                          content_type = 'application/json')
            return response
        else:
            response = app.response_class(response = json.dumps({"message": "NOT FOUND"}, indent = 4),
                                          status = 404,
                                          content_type = 'application/json')
            return response


api.add_resource(Comments, "/comment")
api.add_resource(NComments, "/n-comments")

if __name__ == '__main__':
    db_connection.create_tables()
    app.run(debug = True, host = '0.0.0.0', port = 5200)
