import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS records (ID INTEGER PRIMARY KEY AUTOINCREMENT,type1 text,name text, mask text, temperature real, sp02 real, date_time text, contact text)"
cursor.execute(create_table)

sel="SELECT * FROM records"
for row in cursor.execute(sel):
    print(row)
connection.commit()
connection.close()
