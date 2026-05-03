from db import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT 1")
print(cursor.fetchone())

conn.close()