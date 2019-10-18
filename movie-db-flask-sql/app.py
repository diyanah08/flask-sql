from flask import Flask, render_template, request, redirect, url_for
import pymysql
import os

connection = pymysql.connect(
    host='localhost',
    user='admin',
    password='password',
    database='moviedb'
    )
 

app = Flask(__name__)

@app.route('/')
def home():
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    sql = "SELECT * FROM movie"
    cursor.execute(sql)
    return render_template("index.template.html", results=cursor)
    
@app.route('/actors')
def actors():
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    sql = "SELECT * FROM actor"
    cursor.execute(sql)
    return render_template("actor.template.html", results=cursor)
    
@app.route('/search-movies', methods=['GET'])
def searchMovie():
    return render_template("search-movie.template.html")
    
@app.route('/search-movies', methods=['POST'])
def search():
    connection = pymysql.connect(host = 'localhost',
        user='admin',
        password='password',
        database='moviedb'
        )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    search_terms = request.form['search']
    
    sql = "SELECT * FROM movie WHERE Title LIKE '%{}%'".format(search_terms)
    cursor.execute(sql)
    return render_template("search-movie.template.html", results=cursor)
    
if __name__ == '__main__':
	app.run(host=os.environ.get('IP'),
	port=int(os.environ.get('PORT')),
	debug=True)