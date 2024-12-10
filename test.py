import sqlite3
conn = sqlite3.connect("fms.db")
cursor = conn.cursor()
cursor.execute('''
     SELECT * FROM donations; 
''') # donations

donations_report = cursor.fetchall()
conn.close()

print(donations_report)