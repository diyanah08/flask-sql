import pymysql

connection = pymysql.connect(host = 'localhost',
    user='admin',
    password='password',
    database='chinrook'
    )

artist_name = input("Please enter the artist name > ")    
    
cursor = connection.cursor(pymysql.cursors.DictCursor)
cursor.execute("SELECT MAX(ArtistId) FROM Artist")
max_id = cursor.fetchone()[0]
next_id = max_id + 1

sql = "INSERT INTO Artist (ArtistId, Name) VALUES ({}, '{}')".format(next_id, artist_name)
cursor.execute(sql)

connection.commit() #only when there is changes in database