# Run the Agent

from langchain_core.messages import HumanMessage
from graph_builder import build_agent_graph

app = build_agent_graph()

# query = "What is refund pol



query =[
    "Raise a ticket with id 3526",
    "order the product with given product id 2",
    "Send email to iamitkumar2007@gmail.com by saying your order has been successfully placed",
    "I want my refund",
    "Customer support",
    "After how many days refund gets issued?",
    "How to update billing information?",
    "Contact customer support"
]

# ?"
# query = "raise a ticket for this issue"
<<<<<<< HEAD
query = "email"
=======
# query = "Raise a ticket with id 3526"
# query = "order the product with given product id 2"
# query = "Send email to stakeholder with message like we need few more details abour the requirements"
# query = "Customer support"
>>>>>>> a2fb18ed5c20ef7939c7fbf1e9fce7a9bb5d36c5

for q in query:

    final_state = app.invoke(
        {"messages":[HumanMessage(content=query)],"query":q,"result":""},
         config = {"configurable":{"thread_id":"cust-123"}}
    )
    print("Final Answer:  ",final_state["result"])