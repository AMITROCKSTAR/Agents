import sqlite3

from dotenv import load_dotenv
import re

load_dotenv()

#Define Agent Tools

# def search_kb(query:str)->str:

    
def query_db(query:str)-> str:
    try:
        conn = sqlite3.connect("orders.db")
        cursor = conn.cursor()

        # Extract order_id from user query
        match = re.search(r"\b\d+\b",query)
        order_id = match.group() if match else "12345"

        cursor.execute("SELECT customer_name FROM ordering where order_id=?",(order_id,))
        row = cursor.fetchone()
        # print("row: --- >",row)
        conn.close()

        if row :
            return f"order # {order_id} customer_name :{row[0]}"
        print(f"order # {order_id} not found")
    
        return f"order #{order_id} not found"
        
    except Exception as e:
        return f" DB error : {e}"