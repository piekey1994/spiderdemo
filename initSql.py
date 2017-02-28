import sqlite3

conn = sqlite3.connect('test.db')
print("Opened database successfully")

conn.execute('''CREATE TABLE food
       (id varchar(50) PRIMARY KEY NOT NULL,
       name varchar(100) NOT NULL,
       href text not null,
       usetime varchar(10),
       taste varchar(50),
       img text not null,
       technology varchar(10),
       steps int,
       hot int,
       time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);''')
conn.execute('''CREATE TABLE label
       (id INTEGER PRIMARY KEY NOT NULL,
       fid varchar(50) NOT NULL,
       label varchar(50) NOT NULL,
       time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);''')       
print("Table created successfully")
conn.close()