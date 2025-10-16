# Define Graph Nodes
import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
from langchain_groq import ChatGroq
from agent_state import AgentState
from tools import tools
import os
from dotenv import load_dotenv 
load_dotenv()
## LLM Setup

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0,groq_api_key=os.getenv("GROQ_API_KEY"))

def prompt_node(state: AgentState)->AgentState:
    prompt = ChatPromptTemplate.from_messages([
        ("system","You are a smart assistant that routes user queries to the correct tool."
        """ Available tools:
                             1. KnowledgeBase - For answering FAQs, support information, policies, product info, or general help.
                             2. TicketingSystem - For creating, updating, or checking support tickets.
                             3. Database - For checking order details, order status, or database lookups.
                             4. Email - For sending emails or notifications.

                             Classify the user's intent carefully:
                             - If the query is informational (e.g., "customer support", "return policy", "refund help"), use Knowledge_Base.
                             - If the user requests help, complains, or wants a ticket created (e.g., "raise a complaint", "file a support ticket"), use Ticketing_System.
                             - If the query mentions order ID, shipment, or database keywords (e.g., "order 12345", "my purchase"), use Database_Query.
                             - If the query involves sending an email (e.g., "email me confirmation"), use Email_System.

                             
                        
         Reply ONLY in this JSON format: 
         {{"tool": "KnowledgeBase/Database/TicketingSystem/Email","reason":"short explanation"}}"""),
        ("human","{query}")

    ])

    chain = prompt | llm
    response = chain.invoke({"query":state["query"]})
    state["messages"].append(response)

    # Parse JSON safely

    try:
        decision = json.loads(response.content)
        #print("decision-",decision)
        state["selected_tool"] = decision.get("tool")
        state["tool_reason"]= decision.get("reason")

    except Exception as e:
        state["selected_tool"]=None
        state["tool_reason"]="LLM did not return valid JSON"
        
    return state

def tool_node(state:AgentState)->AgentState:

    tool_name = state.get("selected_tool")

    print("tool",tool_name)
    if tool_name in tools:
    
        result = tools[tool_name](state["query"])

    else:
        result = "Sorry, I couldn't resolve this. Escalating to human support"
        

    state["result"]=result
    state["messages"].append(AIMessage(state["query"]))
    return state

