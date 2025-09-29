import smtplib
from email.mime.text import MIMEText
import requests
import sqlite3
import os
from dotenv import load_dotenv
import re
import base64

load_dotenv()

# create the mail content
msg = MIMEText("Hello , this is a est email", "plain")
msg['Subject'] = "Test Email"
msg["From"] = "sender@gmail.com"
msg['To']="reciever@gmail.com"


#Define Agent Tools

def search_kb(query:str)->str:
    url = "https://api.duckduckgo.com/"
    params ={"q":query,"format":"json"}
    
    try:
        r = requests.get(url,params = params,timeout=10)
        r.raise_for_status()
        data = r.json()
        abstract = data.get("Abstract",)
        if abstract:
            return abstract
        
        related = data.get("related text",[])
        if related:
            return related[0].get("Text","No relavent input found")
        return "No relavent input found"
    
    except Exception as e:
        return f"Knowledge base error : {e}"

    
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
        url = os.getenv("TICKET_API_URL", "https://jsonplaceholder.typicode.com/posts")
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
        print("response",response.json())
        if response.status_code in (200,201):
            print("Token",token)
            return f"Ticket created with id : {response.json().get('id','NA')}"

    except Exception as e:
        return f"Key error: {e}" 
    

def send_email(message:str)->str:
    try:
        sender = os.getenv("EMAIL_SENDER")
        recipient = os.getenv("EMAIL_RECIPIENT")
        password = os.getenv("EMAIL_PASSWORD")

        msg = MIMEText(message)

        msg["Subject"] = "Support Response"
        msg["From"] = sender
        msg["To"] = recipient
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
             server.login(sender, password)
             server.sendmail(sender, recipient, msg.as_string())

        return f"Email sent to {recipient}"
    except Exception as e:
       return f"Email failed: {str(e)}"

  #  return f"Email sent: {message}"

## Tools dictionary

tools = {
    "KnowledgeBase": search_kb,
    "Database":query_db,
    "TicketingSystem": create_ticket,
    "Email": send_email
}