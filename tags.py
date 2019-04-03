from flask import Flask, request, jsonify
import articles_db
import users_db, db_connection, tags_db
import json
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
from passlib.hash import sha256_crypt

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()


@auth.verify_password
def verify(username, password):
    passwd = users_db.get_user_details(username)
    if passwd:
        passwd = passwd[0]
        passwd = passwd[2]
        if sha256_crypt.verify(password, passwd):
            return True
        else:
            return False
    else:
        return False


class Tags(Resource):

    @auth.login_required
    def post(self):
        data = request.get_json()
        tag_name = data['tag_name']
        url = data['url']
        if tag_name == '' or url == '':
            response = app.response_class(response=json.dumps({"message": "Bad Request"}, indent=4),
                                          status=400,
                                          content_type='application/json')
            return response
        article_url = articles_db.get_article_by_url(url)
        if not article_url:
            response = app.response_class(response=json.dumps({"message": "NOT FOUND"}, indent=4),
                                          status=404,
                                          content_type='application/json')
            return response
        tags_db.post_tag(tag_name, url)
        response = app.response_class(response=json.dumps({"message": "Created"}, indent=4),
                                      status=201,
                                      content_type='application/json')
        return response

    @auth.login_required
    def delete(self):
        data = request.get_json()
        url = data['url']
        if url == '':
            response = app.response_class(response=json.dumps({"message": "BAD REQUEST"}, indent=4),
                                          status=400,
                                          content_type='application/json')
            return response
        tag = tags_db.get_tag_details(url)
        if not tag:
            response = app.response_class(response = json.dumps({"message": "NOT FOUND"}, indent = 4),
                                          status = 404,
                                          content_type = 'application/json')
            return response
        tag = tag[0]
        tags_db.delete_tag(tag[0])
        response = app.response_class(response=json.dumps({"message": "OK"}, indent=4),
                                      status=200,
                                      content_type='application/json')
        return response

    def get(self):
        data = request.get_json()
        tag_name = data['tag_name']
        if tag_name == '':
            response = app.response_class(response=json.dumps({"message": "BAD REQUEST"}, indent=4),
                                          status=400,
                                          content_type='application/json')
            return response
        tags = tags_db.get_tag_by_tag_name(tag_name)
        if not tags:
            response = app.response_class(response=json.dumps({"message": "NOT FOUND"}, indent=4),
                                          status=404,
                                          content_type='application/json')
            return response
        return jsonify({"Tags": tags})


class TagsByURL(Resource):
    def get(self):
        data = request.get_json()
        url = data['url']
        if url == '':
            response = app.response_class(response=json.dumps({"message": "BAD REQUEST"}, indent=4),
                                          status=400,
                                          content_type='application/json')
            return response
        tags = tags_db.get_tags_by_url(url)
        if not tags:
            response = app.response_class(response=json.dumps({"message": "NOT FOUND"}, indent=4),
                                          status=404,
                                          content_type='application/json')
            return response
        return jsonify({"Tags": tags})

api.add_resource(Tags, '/tags')
api.add_resource(TagsByURL, '/tags_url')

if __name__ == '__main__':
    db_connection.create_tables()
    app.run(debug = True, host = '0.0.0.0')
