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
# @app.route('/tag/post', methods = ['POST'])
    def post(self):
        data = request.get_json()
        tag_name = data['tag_name']
        url = data['url']
        if tag_name == '' or url == '':
            return jsonify({"Message": "BAD REQUEST"}), 400
        auth = authorization()
        article_url = articles_db.get_article_by_url(url)
        if not article_url:
            return jsonify({"Message": "Not Found"}), 404
        if auth is not None:
            if auth:
                tags_db.post_tag(tag_name, url)
                return jsonify({"Message": "Created"}), 201
            else:
                    return jsonify({"Message": "Could not verify your login!"}), 401
        else:
            return jsonify({"Message": "NOT FOUND"}), 404

    def delete(self):
        data = request.get_json()
        auth = authorization()
        url = data['url']
        if url == '':
            return jsonify({"Message": "BAD REQUEST"}), 400
        if auth is not None:
            if auth:
                tag = tags_db.get_tag_details(url)
                if not tag:
                    print(1)
                    return jsonify({"Message": "Not Found"})
                tag = tag[0]
                tags_db.delete_tag(tag[0])
                return jsonify({"Message": "OK"}), 200
            else:
                return jsonify({"Message": "Unauthorized Access"}), 401
        else:
            return jsonify({"Message": "Could not verify your login!"}), 401

    def get(self):
        data = request.get_json()
        tag_name = data['tag_name']
        if tag_name == '':
            return jsonify({"Message": "BAD REQUEST"}), 400
        tags = tags_db.get_tag_by_tag_name(tag_name)
        if not tags:
            return jsonify({"Message": "Not Found"}), 404
        return jsonify({"Tags": tags})


class TagsByURL(Resource):
    def get(self):
        data = request.get_json()
        url = data['url']
        if url == '':
            return jsonify({"Message": "BAD REQUEST"}), 400
        tags = tags_db.get_tags_by_url(url)
        if not tags:
            return jsonify({"Message": "Not Found"})
        return jsonify({"Tags": tags})

api.add_resource(Tags, '/tags')
api.add_resource(TagsByURL, '/tags_url')

# @app.route('/tag/retrieve_metadata')
# def retrieve_metadata():
#     data = request.get_json()
#     n = data['no_of_tags']
#     n_tags = tags_db.get_tags_metadata(n)
#     with open('tags_metadata.txt', 'w') as tag:
#         json.dump(n_tags, tag, indent = 4)
#     return jsonify({"Message": "OK"}), 200


if __name__ == '__main__':
    db_connection.create_tables()
    app.run(debug = True, host = '0.0.0.0', port = 5003)




# @app.route('tag/add_article_new_tag')
# def add_article():
#     data = request.get_json()
#     return ''
#
# @app.route('tag/all_article')
# def all_article():
#     data = request.get_json()
#     tag_name = data['tag_name']
#     tag = tags_db.get_tag(tag_name)
#     if tag == articles_db.get_n_articles(data):
#         articles_db.get_n_articles(data)
#         with open('articles.txt', 'w') as tag:
#             json.dump(tag, articles_db.get_n_articles(data), indent=4)
#         return jsonify({"Message": "OK"}), 200
#     else:
#        return jsonify({"Message": "Unauthorized Access"}), 401
#
