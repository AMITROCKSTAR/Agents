# Run the Agent

from langchain_core.messages import HumanMessage
from graph_builder import build_agent_graph

app = build_agent_graph()

# query = "What is refund pol





# ?"
# query = "raise a ticket for this issue"
query = "order"

final_state = app.invoke(
    {"messages":[HumanMessage(content=query)],"query":query,"result":""},
     config = {"configurable":{"thread_id":"cust-123"}}
)

print("Final Answer:  ",final_state["result"])