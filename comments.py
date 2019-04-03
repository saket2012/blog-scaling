from db_connection import get_db
from flask import request, Flask, jsonify
from datetime import datetime
import users_db
import json
from flask_restful import Api, Resource
from flask_httpauth import HTTPBasicAuth
from functools import wraps
from passlib.hash import sha256_crypt

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

@auth.verify_password
def verify(username, password):
    global author
    passwd = users_db.get_user_details(username)
    if passwd:
        passwd = passwd[0]
        passwd = passwd[2]
        if sha256_crypt.verify(password, passwd):
            return True
        else:
            author = "Anonymous Coward"
            return False
    else:
        author = "Anonymous Coward"
        return False


def check_auth(username, password):
    return verify(username,password)

def authenticate():
    response = app.response_class(response = json.dumps({"message": "NOT FOUND"}, indent = 4),
                                  status = 404,
                                  content_type = 'application/json')
    return response


def author(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        global author
        if not auth or not check_auth(auth.username, auth.password):
            author = 'Anonymous Coward'
        else:
            author= auth.username
        return f(*args, **kwargs)
    return decorated

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
        return False



def get_article_id(data):
    title = data['title']
    author = data['author']
    conn = get_db()
    c = conn.cursor()

    c.execute("""SELECT * from articles where title == (?) and author == (?)""", (
        title, author))
    row = c.fetchone()
    article_id = row[0]
    return article_id


class Comments(Resource):

    @author
    def post(self):
        data = request.get_json()
        title = data['title']
        author_name = data['author']
        comment = data['comment']
        post_time = datetime.now()
        success_flag = 0

        if author == "Anonymous Coward":
            user_id = -1
            display_name = "Anonymous Coward"
        else:
            user_id = data['user_id']
            display_name = data['display_name']

        conn = get_db()
        c = conn.cursor()
        try:
            c.execute("""SELECT * from articles where title == (?) and author == (?)""", (
                title, author_name))
            row = c.fetchone()
            article_id = row[0]
        except Exception:
            response = app.response_class(response=json.dumps({"message": "Article Not Found"}, indent=4),
                                          status=404,
                                          content_type='application/json')
            return response

        if row != None:
            try:
                c.execute("""INSERT into comments(user_id, article_id, display_name, comment, post_time) values (?,?,?,?,?)
                """, (user_id, article_id, display_name, comment, post_time))
                conn.commit()
                success_flag = 1

            except Exception:
                conn.rollback()

        if success_flag == 1:
            data['user_id'] = user_id
            data['display_name'] = display_name
            resp = jsonify(data)
            resp.status_code = 201
            return resp
        else:
            response = app.response_class(response=json.dumps({"message": "Failed to add Comment"}, indent=4),
                                          status=409,
                                          content_type='application/json')
            return response


    def delete(self):
        # Delete an individual comment
        data = request.get_json()
        comment_id = data['comment_id']
        conn = get_db()
        c = conn.cursor()
        c.execute("""SELECT * from comments where comment_id == (?)""", (
            comment_id))
        row = c.fetchone()
        if row:
            c.execute("""DELETE from comments where comment_id  == (?)""", (
                comment_id))
            conn.commit()
            response = app.response_class(response=json.dumps({"message": "OK"}, indent=4),
                                          status=200,
                                          content_type='application/json')
            return response
        else:
            response = app.response_class(response=json.dumps({"message": "Comment Not Found"}, indent=4),
                                          status=404,
                                          content_type='application/json')
            return response


    def get(self):
        "Retrieve the number of comments on a given article"

        data = request.get_json()
        # title = data['title']
        # author = data['author']
        article_id = data['article_id']
        conn = get_db()
        c = conn.cursor()

        try:
            c.execute('SELECT COUNT(*) from comments where article_id == (?)', (
                article_id))
            rows = c.fetchone()
            return jsonify(rows), 200
        except Exception:
            conn.rollback()
            error_msg = "Failed to retrieve the Number of Comments"
            return jsonify(error_msg), 409


class N_Comments(Resource):
    def get(self):
        "Retrieve the n most recent comments on a URL"

        data = request.get_json()
        author = data['author']
        title = data['title']
        n = data['n']

        conn = get_db()
        c = conn.cursor()
        c.execute("""SELECT * from articles where title == (?) and author == (?)""", (
            title, author))
        row = c.fetchone()
        article_id = row[0]
        if row != None:
            try:
                c.execute("""SELECT * from comments where article_id  == (?) ORDER BY post_time DESC LIMIT (?)""", (
                    article_id , n))
                rows = c.fetchall()
                return jsonify(rows), 200
            except Exception:
                conn.rollback()
                return jsonify(message="Failed to get comments"), 409

api.add_resource(Comments, "/comments")
api.add_resource(N_Comments, "/ncomments")

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5300)
