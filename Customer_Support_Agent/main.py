# Run the Agent
from fastapi import FastAPI,Form
from fastapi.responses import JSONResponse
from langchain_core.messages import HumanMessage
from graph_builder import build_agent_graph
import uvicorn

app = build_agent_graph()

api = FastAPI(title="Customer Support Agent API")

@api.post("/query/")
def user_query(query: str = Form(...)):
    try:
        final_state = app.invoke(
            {"messages":[HumanMessage(content=query)],"query":query,"result":""},
            config={"configurable":{"thread_id":"cust-123"}}
        )
        return JSONResponse({
            "query": query,
            "response": final_state["result"]
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    

if __name__ == "__main__":
    uvicorn.run("main:api", host="127.0.0.0", port=8000, reload=True)