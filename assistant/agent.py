import os
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from .tools import search_products_tool, check_order_status_tool

def get_shopping_assistant():
    llm = ChatGroq(
        groq_api_key=os.getenv('GROQ_API_KEY'),
        model_name="llama-3.3-70b-versatile",
        temperature=0.3
    )
    tools = [search_products_tool, check_order_status_tool]
    
    agent = create_react_agent(llm, tools)
    
    return agent