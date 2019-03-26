from flask import Flask, request, jsonify
import articles_db
import users_db, db_connection, tags_db
import json
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


def authorization():
    auth = request.authorization
    if auth:
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


class Tags(Resource):
    def post(self):
        data = request.get_json()
        tag_name = data['tag_name']
        url = data['url']
        if tag_name == '' or url == '':
            response = app.response_class(response=json.dumps({"message": "Bad Request"}, indent=4),
                                          status=400,
                                          content_type='application/json')
            return response
        auth = authorization()
        if auth is not None:
            if auth:
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
            else:
                response = app.response_class(response=json.dumps({"message": "CONFLICT"}, indent=4),
                                              status=409,
                                              content_type='application/json')
                return response
        else:
            response = app.response_class(response=json.dumps({"message": "NOT FOUND"}, indent=4),
                                          status=404,
                                          content_type='application/json')
            return response

    def delete(self):
        data = request.get_json()
        auth = authorization()
        url = data['url']
        if url == '':
            response = app.response_class(response=json.dumps({"message": "BAD REQUEST"}, indent=4),
                                          status=400,
                                          content_type='application/json')
            return response
        if auth is not None:
            if auth:
                tag = tags_db.get_tag_details(url)
                if not tag:
                    return jsonify({"Message": "Not Found"})
                tag = tag[0]
                tags_db.delete_tag(tag[0])
                response = app.response_class(response=json.dumps({"message": "OK"}, indent=4),
                                              status=200,
                                              content_type='application/json')
                return response
            else:
                response = app.response_class(response=json.dumps({"message": "UNAUTHORIZED ACCESS"}, indent=4),
                                              status=401,
                                              content_type='application/json')
                return response
        else:
            response = app.response_class(response=json.dumps({"message": "UNAUTHORIZED ACCESS"}, indent=4),
                                          status=401,
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
