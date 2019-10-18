from flask import Flask, render_template, request, redirect, url_for
import pymysql
import os

app = Flask(__name__)

@app.route('/')
def home():
    connection = pymysql.connect(
        host='localhost',
        user='admin',
        password='password',
        database='chinrook'
        )
        
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    sql = "SELECT * FROM Employee"
    cursor.execute(sql)
    return render_template("index.template.html", results=cursor)
    
@app.route('/artist')
def artists():
    connection = pymysql.connect(
        host='localhost',
        user='admin',
        password='password',
        database='chinrook'
        )
        
    cursor = connection.cursor(pymysql.cursors.DictCursor)
     
    sql = "SELECT * FROM Artist"
    cursor.execute(sql)
    return render_template('artists.template.html', results=cursor)
     
@app.route('/album/<artistId>')
def albums(artistId):
    connection = pymysql.connect(
        host='localhost',
        user='admin',
        password='password',
        database='chinrook'
        )
        
    cursor = connection.cursor(pymysql.cursors.DictCursor)
     
    sql = "SELECT * FROM Artist Where ArtistId = {}".format(artistId)
    cursor.execute(sql)
    artist = cursor.fetchone()
     
    sql = "SELECT * FROM Album WHERE ArtistId = {}".format(artistId)
    cursor.execute(sql)
    return render_template('albums.template.html', results=cursor, artist=artist)
    
@app.route('/album/track/<albumId>')
def track(albumId):
    connection = pymysql.connect(
        host='localhost',
        user='admin',
        password='password',
        database='chinrook'
        )
        
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    sql = "SELECT * FROM Album Where AlbumId = {}".format(albumId)
    cursor.execute(sql)
    album = cursor.fetchone()
     
    sql = "SELECT * FROM Track WHERE AlbumId = {}".format(albumId)
    cursor.execute(sql)
    return render_template('tracks.template.html', results=cursor, album=album)
    
@app.route('/combined')
def combined():
    connection = pymysql.connect(
        host='localhost',
        user='admin',
        password='password',
        database='chinrook'
        )
        
    employeeCursor = connection.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM Employee"
    employeeCursor.execute(sql)
    albumCursor = connection.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM Album"
    albumCursor.execute(sql)
    
    return render_template("combined.template.html", employeeResults=employeeCursor, albumResults = albumCursor)
    
@app.route('/search', methods=['GET'])
def searchAlbum():
    return render_template("search-album.template.html")
    
@app.route('/search', methods=['POST'])
def search():
    connection = pymysql.connect(host = 'localhost',
        user='admin',
        password='password',
        database='chinrook'
        )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    search_terms = request.form['search']
    
    sql = "SELECT * FROM Album INNER JOIN Artist ON Album.ArtistID = Artist.ArtistID WHERE Title LIKE '%{}%' OR Artist.Name LIKE '%{}%'".format(search_terms, search_terms)
    cursor.execute(sql)
    return render_template("search-album.template.html", results=cursor)
    
@app.route('/employee', methods=['GET'])
def searchEmployee():
    return render_template("search-employee.template.html")
    
@app.route('/employee', methods=['POST'])
def searchResults():
    connection = pymysql.connect(host = 'localhost',
        user='admin',
        password='password',
        database='chinrook'
        )
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    name_terms = request.form['name']
    title_terms = request.form['title']
    
    sql = "SELECT * FROM Employee WHERE FirstName LIKE '%{}%' OR LastName LIKE '%{}%' OR Title LIKE '%{}%'".format(name_terms, name_terms, title_terms)
    cursor.execute(sql)
    return render_template("search-employee.template.html", results=cursor)
    
@app.route('/new-album')
def show_new_album_form():
    connection = pymysql.connect(host = 'localhost',
        user='admin',
        password='password',
        database='chinrook'
        )
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    sql = "SELECT * FROM Artist"
    cursor.execute(sql)
    
    return render_template("add-new-album.template.html", artists=cursor)
    
@app.route('/new-album', methods=['POST'])
def process_add_album():
    artist = request.form['artist']
    album = request.form['album']
    
    connection = pymysql.connect(host = 'localhost',
        user='admin',
        password='password',
        database='chinrook'
        )
    cursor = connection.cursor()
    
    sql = "SELECT MAX(AlbumId) FROM Album"
    cursor.execute(sql)
    
    max_id = cursor.fetchone()[0]
    next_id = max_id + 1
    
    sql = "INSERT INTO Album (AlbumId, Title, ArtistId) VALUES ({}, {}, {})".format(next_id, album, artist)
    
    cursor.execute(sql)
    
    connection.commit()
    
    return "done"
    
# @app.route('/edit-album/<album_id>')
# def show_edit_album_form(album_id):
#     connection = pymysql.connect(host = 'localhost',
#         user='admin',
#         password='password',
#         database='chinrook'
#         )
#     cursor = connection.cursor(pymysql.cursors.DictCursor)
    
#     artistCursor = connection.cursor(pymysql.cursors.DictCursor)
#     sql = "SELECT * FROM Artist"
#     artistCursor.execute(sql)
    
    
#     sql = "SELECT * FROM Album WHERE AlbumId = {}".format(album_id)
#     cursor.execute(sql)
    
#     album = cursor.fetchone()
    
#     return render_template('edit-album-form.template.html', album=album, artistCursor=artistCursor)

@app.route('/edit-artist/<ArtistId>')
def edit_artist(ArtistId):
    connection = pymysql.connect(host = 'localhost',
        user='admin',
        password='password',
        database='chinrook'
        )
        
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM Artist WHERE ArtistId = {}".format(ArtistId))
    artist = cursor.fetchone()
    return render_template('edit-artist.template.html', artist=artist)
    
@app.route('/edit-artist/<ArtistId>', methods=['POST'])
def update_artist(ArtistId):
    connection = pymysql.connect(host = 'localhost',
        user='admin',
        password='password',
        database='chinrook'
        )
    
    artist_name = request.form['change-artist']
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute("UPDATE Artist SET Name = '{}' WHERE ArtistId = {}".format(artist_name, ArtistId))
    
    connection.commit()
    return redirect(url_for('artists'))
    
    

if __name__ == '__main__':
	app.run(host=os.environ.get('IP'),
	port=int(os.environ.get('PORT')),
	debug=True)
