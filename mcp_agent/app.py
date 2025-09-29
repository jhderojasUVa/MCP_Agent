from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI # Or any tool-calling LLM (e.g., Gemini)

# 1. Define the connection parameters for your MCP server
MCP_CONFIG = {
    "coffee_server": {
        "url": "http://localhost:3000",  # Replace with your server's URL
        "transport": "streamable_http",
    }
}

# 2. Initialize the MultiServerMCPClient
mcp_client = MultiServerMCPClient(MCP_CONFIG)

# 3. Define the LLM (Large Language Model)
# The LLM is the 'brain' that decides *when* to call the tool.
llm = ChatGoogleGenerativeAI(model="gemini-pro") # A model with strong tool-calling capabilities

# 4. Asynchronously load the tools from your server
async def build_agent():
    # Load all tools exposed by the server (e.g., 'get_coffee_types')
    tools = await mcp_client.get_tools() 
    
    # 5. Create the Agent
    # The ReAct Agent uses the LLM to reason about which tool to call.
    agent_executor = create_react_agent(llm, tools)
    
    print(f"Agent successfully loaded tools: {[t.name for t in tools]}")
    return agent_executor

# Run the setup and test the agent
import asyncio
agent = asyncio.run(build_agent()) 

# Example Usage:
user_query = "Can you list three popular types of coffee?"
response = asyncio.run(agent.ainvoke({"messages": [("user", user_query)]}))

# The Agent will now follow these steps:
# 1. Reason: User wants coffee types, I have the 'get_coffee_types' tool.
# 2. Call Tool: It sends the function call to the 'coffee_server'.
# 3. Get Result: The MCP server responds with the list (e.g., "Espresso, Latte, Cappuccino").
# 4. Final Answer: The Agent formats the result into a human-readable answer.
# 5. Respond: "The popular coffee types are Espresso, Latte, and Cappuccino."

print(response)