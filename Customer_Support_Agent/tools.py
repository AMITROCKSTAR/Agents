import smtplib
from email.mime.text import MIMEText
import requests
import sqlite3
import os
from dotenv import load_dotenv
import re
import base64

from Tools import Search_kb
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
        # print("order_id",order_id)
        # print("cursor",cursor)
        # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        # tables = cursor.fetchall()

        # print("Tables in database:", tables)
        # cursor.execute("SELECT * FROM ordering")
        # print("Result",cursor.fetchall())
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

def create_ticket(issue:str)->str:
    try:
        url = os.getenv("TICKET_API_URL", "https://amitrock9889.atlassian.net/rest/api/3/issue")
        token = os.getenv("TICKET_API_TOKEN", None)
        email = os.getenv("JIRA_EMAIL")
        print("token check",url)

        #Encode email:token in Base64

        auth_bytes = f"{email}:{token}".encode("ascii")
        auth_64 = base64.b64encode(auth_bytes).decode("ascii")

        headers = {"Authorization":f"Basic {auth_64}", "Content-Type":"application/json"}
        # Payload to create a Jira ticket
        payload = {
            "fields": {
                "project": {"key": "KAN"},       # Replace with your project key
                "summary": issue,
                "description": issue,
                "issuetype": {"name": "Task"}    # Can be "Task", "Bug", "Story", etc.
            }
        }
        response = requests.post(url,json=payload, headers=headers)
        print("response____",response)
        print("response",response.json())
        if response.status_code in (200,201):
            print("Token",token)
            return f"Ticket created with id : {response.json().get('id','NA')}"

    except Exception as e:
        return f"Key error: {e}" 
    

def send_email(query:str)->str:
    # recipient:str,subject:str,body:str
    ## Use regex to find recipient , subject and body
    ##query : "Send email to iamitkumar2007@gmail.com by saying your order has been successfully placed"
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    print("Pattern",pattern)
    text = re.findall(pattern,query)
    recipient = ','.join(text)
    print("Recipient",str(recipient))
    
    ## Converting comma seperated string
    query = query.split()
    print("query",query)
    ## Finding order status related value , like delivered,ordered,placed ,etc.
    status = ["Ship","Shipped","Shipping","Order","Ordered","Placed","Place","Delivered","Delivery"]
    matched_status = {"ship":"Shipped","shipped":"Shipped","order":"Ordered","ordered":"Ordered","placed":"Placed","delivered":"Delivered","delivery":"Delivered"}
    status_value =""
    for s in status:
        
        for q in query:
            # print("---",q)
            if q.upper()==s.upper():
                status_value = s.lower()
                break
    
    print("status_value",status_value)
    body = f"Your order has been successfully {matched_status[status_value]}"
    subject = f"Order Status"
    try:
        msg = MIMEText(body)
        msg["From"] = os.getenv("EMAIL_SENDER")
        msg["To"] = recipient
        msg["Subject"] = subject
        password = os.getenv("EMAIL_PASSWORD")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
             server.login(msg["From"], password)
             server.send_message(msg)

        return {"status":"success","message":f"{body}"}
    except Exception as e:
       return f"Email failed: {str(e)}"

  #  return f"Email sent: {message}"

## Tools dictionary

tools = {
    "KnowledgeBase": Search_kb.search_kb,
    "Database":query_db,
    "TicketingSystem": create_ticket,
    "Email": send_email
}

