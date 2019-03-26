from db_connection import get_db
from flask import request, Flask, jsonify
from datetime import datetime
import users_db
import json
from flask_restful import Api, Resource
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
    def post(self):
        # Add Comment

        data = request.get_json()
        title = data['title']
        author = data['author']
        comment = data['comment']
        post_time = datetime.now()
        success_flag = 0

        auth = authorization()
        if auth:
            user_id = data['user_id']
            display_name = data['display_name']
        else:
            user_id = -1
            display_name = "Anonymous  Coward"

        conn = get_db()
        c = conn.cursor()
        try:
            c.execute("""SELECT * from articles where title == (?) and author == (?)""", (
                title,author))
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


# curl --include --verbose --request DELETE --header 'Content-Type: application/json' --data '{"comment_id" : "1"}' http://localhost:5000/comments/delete
    def delete(self):
        # Delete an individual comment

        auth = authorization()
        if auth:
            data = request.get_json()
            comment_id = data['comment_id']
            conn = get_db()
            c = conn.cursor()
            try:
                c.execute("""SELECT * from comments where comment_id == (?)""", (
                    comment_id))
                row = c.fetchone()
                if row:
                    c.execute("""DELETE from comments where comment_id  == (?)""", (
                        comment_id))
                    conn.commit()
                    response = app.response_class(response=json.dumps({"message": "Successfully deleted"}, indent=4),
                                                  status=200,
                                                  content_type='application/json')
                    return response
                else:
                    response = app.response_class(response=json.dumps({"message": "Record Not Found"}, indent=4),
                                                  status=404,
                                                  content_type='application/json')
                    return response
            except Exception:
                conn.rollback()
                response = app.response_class(response=json.dumps({"message": "Failed"}, indent=4),
                                              status=409,
                                              content_type='application/json')
                return response
        else:
            error_msg = "Need User Authentication to perform the DELETE Operation"
            response = app.response_class(response=json.dumps({"message": "Need User Authentication to perform the DELETE Operation"}, indent=4),
                                          status=401,
                                          content_type='application/json')
            return response

# curl --include --verbose --request GET --header 'Content-Type: application/json' --data '{"article_id" : "3"}' http://localhost:5000/comments/getnumber
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


# curl --include --verbose --request GET --header 'Content-Type: application/json' --data '{"article_id" : "3", "n" : "10"}' http://localhost:5000/comments/getn
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
    app.run(debug = True, host = '0.0.0.0')
