import requests
import os
from dotenv import load_dotenv
import re
import base64
load_dotenv()


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
    