import sqlite3

conn = sqlite3.connect('test.db')

conn.execute('''CREATE TABLE user
       (id INTEGER PRIMARY KEY NOT NULL,
       name varchar(50) NOT NULL,
       password varchar(50) NOT NULL,
       time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);''')  

conn.close()