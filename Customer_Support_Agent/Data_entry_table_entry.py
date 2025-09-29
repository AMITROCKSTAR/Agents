import sqlite3

conn = sqlite3.connect("orders.db")
cursor = conn.cursor()

cursor.execute("""create table if not exists Ordering( 
order_id INTEGER PRIMARY KEY AUTOINCREMENT,
customer_name TEXT NOT NULL,
status TEXT NOT NULL,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);""")

rows = [
    ("Amit","Present"),
    ("Sumit", "Absent")
]
cursor.executemany("insert into Ordering(customer_name,status) values (?,?);",rows)
    
conn.commit()
conn.close()