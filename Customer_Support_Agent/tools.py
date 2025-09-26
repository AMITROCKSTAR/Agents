import smtplib
from email.mime.text import MIMEText
import requests
import sqlite3
import os

# create the mail content
msg = MIMEText("Hello , this is a est email", "plain")
msg['Subject'] = "Test Email"
msg["From"] = "sender@gmail.com"
msg['To']="reciever@gmail.com"


#Define Agent Tools

def search_kb(query:str)->str:
    url = "https://api.duckduckgo.com/"
    params ={"q":query,"format":"json"}
    r = requests.get(url,params = params)
    if r.status_code == 200:
        data = r.json()
        return data.get("AbstractText", "No relevant info found in kb.")
    return "Error fetching knowledge base"


def query_db(query:str)-> str:
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()

    cursor.execute("SELECT status FROM orders where order_id=?",("1235"))
    row = cursor.fetchone()
    conn.close()

    if row :
        return f"order #1235 status :{row[0]}"
    return "order not found"


def create_ticket(issue:str)->str:
    url= "https://jsonplaceholder.typicode.com/posts"
    response = requests.post(url,json={"title":"support ticket","body":issue})
    if response.status_code == 201:
        return f"Ticket created with ID {response.json()['id']}"
    return "Error creating ticket."


def send_email(message:str)->str:
    try:
        sender : os.getenv("")
        recipient : os.getenv("")
        password : os.getenv("")

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