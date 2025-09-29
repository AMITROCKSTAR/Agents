# Run the Agent

from langchain_core.messages import HumanMessage
from graph_builder import build_agent_graph

app = build_agent_graph()

# query = "What is refund pol





# ?"
# query = "raise a ticket for this issue"
# query = "Raise a ticket with id 3526"
# query = "order the product with given product id 2"
query = "Send email to stakeholder with message like we need few more details abour the requirements"

final_state = app.invoke(
    {"messages":[HumanMessage(content=query)],"query":query,"result":""},
     config = {"configurable":{"thread_id":"cust-123"}}
)

print("Final Answer:  ",final_state["result"])