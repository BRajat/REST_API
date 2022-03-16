import sqlite3

db = sqlite3.Connection('data.db')
cursor = db.cursor()

# create table
create_table = """CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"""
cursor.execute(create_table)

# create table
create_table = """CREATE TABLE IF NOT EXISTS items (name text, price real)"""
cursor.execute(create_table)

# insert a single value
cursor.execute('Insert into items VALUES ("test",10.99)')

db.commit()
db.close()