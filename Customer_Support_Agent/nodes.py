# Define Graph Nodes
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
from langchain_groq import ChatGroq
from agent_state import AgentState
from tools import tools
import os
from dotenv import load_dotenv 
load_dotenv()
## LLM Setup
# from langchain_groq import ChatGroq

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0,groq_api_key=os.getenv("GROQ_API_KEY"))


def prompt_node(state: AgentState)->AgentState:
    prompt = ChatPromptTemplate.from_messages([
        ("system","You are helpful customer support AI. Decide which tools to call."),
        ("human","{query}")

    ])

    chain = prompt | llm
    response = chain.invoke({"query":state["query"]})
    state["messages"].append(response)
    return state

def tool_node(state:AgentState)->AgentState:
    query_lower = state["query"].lower()
    if "refund" in query_lower:
        result = tools["KnowledgeBase"](state["query"])

    elif "order" in query_lower:
        result = tools["Database"](state["query"])

    elif "ticket" in query_lower:
        result = tools["TicketingSystem"](state["query"])

    elif "email" in query_lower:
        result = tools["Email"](state["query"])

    else:
        f"Sorry I could'nt resolved it Escalating."

    state["result"]=result
    state["messages"].append(AIMessage(state["query"]))
    return state

