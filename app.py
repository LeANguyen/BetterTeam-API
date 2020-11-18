from flask import Flask, render_template, request, jsonify
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

import argument_handler as arg_handler

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
    return "<h4>Get interview job questions with url: E.g.. http://127.0.0.1:5000/accountant</h4>"


@app.route('/all', methods=['GET'])
def get_questions():
    connection = mysql.get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM test.interviews;")
    connection.commit()
    query_value = cursor.fetchall()
    cursor.close()
    return jsonify(query_value)


@app.route('/<string:field>', methods=['GET', 'POST'])
def get_question(field):
    if request.method == "GET":
        connection = mysql.get_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM test.interviews WHERE field = '" + field.title() + "';")
        connection.commit()
        query_value = cursor.fetchall()
        cursor.close()
        return jsonify(query_value)
    return render_template('index.html')


if __name__ == '__main__':
    app.run()