import sqlite3

db = sqlite3.Connection('data.db')

cursor = db.cursor()

# create table
create_table = """CREATE TABLE users (id int, username text, password text)"""

cursor.execute(create_table)

user = (1,'bob','asdf')
# insert single value
insert_query = "INSERT INTO users Values (?,?,?)"

cursor.execute(insert_query, user)
# insert many value
users = [
    (2,'messi','rkj'),
    (3, 'cr','dfs')
]

cursor.executemany(insert_query, users )
# write select query and print
select_query = "Select * from users"

for i in cursor.execute(select_query):
    print(i)

db.commit()

db.close()