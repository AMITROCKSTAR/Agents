import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
import re


load_dotenv()


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
