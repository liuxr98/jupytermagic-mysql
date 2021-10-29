import pymysql

db = pymysql.connect(user='root', password='admin', host='127.0.0.1', port=13306)
cursor = db.cursor()

# query database version
cursor.execute("SELECT VERSION()")
data = cursor.fetchone() 
print ("Database version : %s " % data)

# create database
cursor.execute('CREATE DATABASE PEOPLE')
cursor.execute('USE PEOPLE')
db.commit()

# create table
create_sql = """
    CREATE TABLE EMPLOYEE (
    FIRST_NAME  CHAR(20) NOT NULL,
    LAST_NAME  CHAR(20),
    AGE INT,  
    SEX CHAR(1),
    INCOME FLOAT )
"""
cursor.execute(create_sql)
db.commit()

# insert records into table
insert_sql = """
    INSERT INTO EMPLOYEE(FIRST_NAME, LAST_NAME, AGE, SEX, INCOME)
    VALUES ('Mac', 'Mohan', 20, 'M', 2000)
"""
cursor.execute(insert_sql)
db.commit()

# query records from table
query_sql = """
    SELECT *
    FROM EMPLOYEE
    LIMIT 10
"""
cursor.execute(query_sql)
records = cursor.fetchall()
for record in records:
    print(record)

# update records in table
update_sql = """
    UPDATE EMPLOYEE
    SET AGE = AGE + 1
    WHERE SEX = '{}'
""".format('M')
cursor.execute(update_sql)
db.commit()

# delete records from table
delete_sql = """
    DELETE 
    FROM EMPLOYEE
    WHERE AGE > {}
""".format(15)
cursor.execute(delete_sql)
db.commit()

# close connection
db.close()