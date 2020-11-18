from django.shortcuts import redirect
from flask import Flask, render_template, request, jsonify, url_for
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
import json

app = Flask(__name__)
app.debug = True

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '12345678'
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_PORT'] = 3306
# app.config['MYSQL_DATABASE_CHARSET'] = 'utf8mb4'
mysql = MySQL(app, cursorclass=DictCursor)


@app.route('/')
def index():
    return render_template("this_is_just_for_testing.html")


@app.route('/search', methods=('GET', 'POST'))
def search():
    if request.method == 'GET':
        keyword = request.args.get('keyword')

        if keyword is None:
            return render_template("index.html")

        connection = mysql.get_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM test.interviews WHERE field = '" + keyword + "';")
        connection.commit()
        query_value = cursor.fetchall()
        cursor.close()
        return jsonify(query_value)


@app.route('/all', methods=['GET'])
def get_questions():
    connection = mysql.get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM test.interviews;")
    connection.commit()
    query_value = cursor.fetchall()
    cursor.close()
    return jsonify(query_value)


@app.route('/fields', methods=['GET'])
def get_fields():
    connection = mysql.get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT field FROM test.interviews;")
    connection.commit()
    query_value = cursor.fetchall()
    cursor.close()
    with open('fields.txt', 'w') as outfile:
        json.dump(query_value, outfile)

    with open('fields.json', 'w') as json_file:
        json.dump(query_value, json_file)
    return jsonify(query_value)


# @app.route('/<string:field>', methods=['GET'])
# def get_question(field):
#     connection = mysql.get_db()
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM test.interviews WHERE field = '" + field.title() + "';")
#     connection.commit()
#     query_value = cursor.fetchall()
#     cursor.close()
#     return jsonify(query_value)


if __name__ == '__main__':
    app.run()