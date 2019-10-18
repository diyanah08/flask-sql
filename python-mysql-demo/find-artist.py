import pymysql

connection = pymysql.connect(host = 'localhost',
    user='admin',
    password='password',
    database='chinrook'
    )
    
cursor = connection.cursor(pymysql.cursors.DictCursor)

artist_name = input("Please enter the artist name > ")

sql = "SELECT * FROM Artist WHERE Name LIKE '%{}%'".format(artist_name)
cursor.execute(sql)

for each_result in cursor:
    print(each_result['Name'])