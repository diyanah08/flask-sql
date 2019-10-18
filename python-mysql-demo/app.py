import pymysql

connection = pymysql.connect(host = 'localhost',
    user='admin',
    password='password',
    database='chinrook'
    )
    
# cursor = connection.cursor() #points to one row of the results
# cursor.execute("SELECT * from Employee")
# for row in cursor:
#     print("EmployeeId", row[0]," is ", row[1],row[2])
#     print("EmployeeId:{} is {} {}".format(row[0], row[1], row[2]))
    
cursor = connection.cursor(pymysql.cursors.DictCursor)
cursor.execute("SELECT * from Employee")
for row in cursor:
    print("EmployeeId: {} is {} {}".format(row['EmployeeId'], row['LastName'], row['FirstName']))