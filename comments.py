import json

from flask import request, Flask
from flask_restful import Api, Resource

import articles_db
import comments_db
import db_connection

app = Flask(__name__)
api = Api(app)

class Comments(Resource):

    def post(self, article_id):
        data = request.get_json()
        comment = data['comment']
        username = request.authorization.username
        article = articles_db.get_article_by_id(article_id)
        if article:
            comments_db.post_comment(username, article_id, comment)
            response = app.response_class(response = json.dumps({"message": "CREATED"}, indent = 4),
                                          status = 201,
                                          content_type = 'application/json')
            return response
        else:
            response = app.response_class(response = json.dumps({"message": "NOT FOUND"}, indent = 4),
                                          status = 404,
                                          content_type = 'application/json')
            return response


    def get(self, article_id):
        # Retrieve the number of comments on a given article
        n_comments = comments_db.count_comments(article_id)
        if n_comments > 0:
            no_of_comments = {'Number of comments': n_comments}
            response = app.response_class(response = json.dumps(no_of_comments, indent = 4),
                                          status = 200,
                                          content_type = 'application/json')
            return response
        else:
            response = app.response_class(response = json.dumps({"message": "NOT FOUND"}, indent = 4),
                                          status = 404,
                                          content_type = 'application/json')
            return response


class Delete_Comment(Resource):
    def delete(self, comment_id):
        # Delete an individual comment
        data = request.get_json()
        comment = comments_db.get_comment(comment_id)
        username = request.authorization.username
        if comment:
            rowcount = comments_db.delete_comment(comment_id, username)
            if rowcount == 1:
                response = app.response_class(response=json.dumps({"message": "OK"}, indent=4),
                                              status=200,
                                              content_type='application/json')
                return response
            else:

                    response = app.response_class(response=json.dumps({"message": "NOT FOUND"}, indent=4),
                                                  status=404,
                                                  content_type='application/json')
                    return response
        else:
            response = app.response_class(response = json.dumps({"message": "NOT FOUND"}, indent = 4),
                                          status=404,
                                          content_type='application/json')
            return response

class NComments(Resource):
    def get(self, article_id, recent_comments):
        # Retrieve the n most recent comments for an article
        comments = comments_db.get_comments(article_id, recent_comments)
        if comments:
            response = app.response_class(response = json.dumps(comments, indent = 4),
                                          status = 200,
                                          content_type = 'application/json')
            return response
        else:
            response = app.response_class(response = json.dumps({"message": "NOT FOUND"}, indent = 4),
                                          status = 404,
                                          content_type = 'application/json')
            return response


api.add_resource(Comments, "/comment/<article_id>")
api.add_resource(Delete_Comment, "/delete-comment/<comment_id>")
api.add_resource(NComments, "/n-comments/<article_id>/<recent_comments>")

if __name__ == "__main__":
    db_connection.create_tables()
    app.run(debug = True, host = '0.0.0.0', port = 5200)
