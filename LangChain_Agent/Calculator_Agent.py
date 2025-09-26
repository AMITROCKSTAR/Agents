# from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

from langchain.agents import initialize_agent,AgentType,Tool
import random
import requests

# 1. Engine of the agent
# llm = ChatOpenAI(model="gpt-4o-mini",temperature=0)
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# 2. Define a simple tool
def multiply_numbers(query:str)->str:
    try:
        numbers = [float(x) for x in query.split()]
        result = 1
        for n in numbers:
            result *=n
        return str(result)
    
    except:
        return "Error : Provide numbers seperated by spaces"
    
def name_tool(query: str) -> str:
    jokes = [
        "Why don’t scientists trust atoms? Because they make up everything! 😂",
        "Parallel lines have so much in common… it’s a shame they’ll never meet. 🤣",
        "Why did the math book look sad? It had too many problems! 📘"
    ]
    joke = random.choice(jokes)
    return f"👋 Hello {query.title()}! Here’s a joke for you: {joke}"

# Weather Tool
def get_weather(city: str) -> str:
    try:
        API_KEY = "138b7e69f73bd092072b032de7d5c30d"  # replace with your key
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        resp = requests.get(url)
        data = resp.json()
        if resp.status_code != 200:
            return f"Final Answer: Error – {data.get('message', 'Failed to fetch weather')}"
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"].title()
        return f"Final Answer: 🌍 Weather in {city.title()}: {temp}°C, {desc}"
    except Exception as e:
        return f"Final Answer: Error – {str(e)}"
    
tools =[
    Tool(
        name="Multiplier",
        func=multiply_numbers,
        description="Multiply numbers given in the query. Input should be space seperated numbers"
    ),
    Tool(
        name="JokeGreeter",
        func=name_tool,
        description="Say hello with a funny joke to the name in query."
    ),
    Tool(
        name="Weather",
        func=get_weather,
        description="Get current weather for a city. Input should be a city name."
    )
]

## 3. Create the Agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,  # <-- THIS fixes the crash
    max_iterations=2  # optional: stop looping
)

## 4. Run the Agent
user_input = input("Enter city name: ")
queries = [
    "Multiply 7 3 2",
    f"What's the weather in {user_input}?",
    "Say hello to Amit"
]
final_result={}
for q in queries:
    print("\nUser query:", q)
    print(agent.run(q))
    final_result[q]=agent.run(q)

print(f"Final answer: {final_result}")