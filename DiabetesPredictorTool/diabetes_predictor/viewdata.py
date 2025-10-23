import os
import sqlite3

# __file__ is diabetes_predictor/viewdata.py, so go up one level:
db_path = os.path.join(os.path.dirname(__file__), '..', 'app.db')
db_path = os.path.abspath(db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT * FROM predictions")
rows = cursor.fetchall()

print("Saved Predictions:")
for row in rows:
    print(row)

conn.close()
