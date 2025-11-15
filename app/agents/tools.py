from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from app.config import settings

# doc strings are required
@tool
def get_job_count(input: str) -> str:
    """Returns the number of available jobs"""
    return "There are 5 software engineering internships available right now."

@tool
def get_job_info(job_number: str) -> str:
    """Gets information about a specific job by number (1-5)."""
    jobs = {
        "1": "Google - Software Engineering Intern - Mountain View, CA",
        "2": "Meta - Backend Developer Intern - Menlo Park, CA", 
        "3": "Amazon - SDE Intern - Seattle, WA",
        "4": "Microsoft - Software Engineer Intern - Redmond, WA",
        "5": "Apple - iOS Development Intern - Cupertino, CA"
    }
    
    if job_number in jobs:
        return jobs[job_number]
    else:
        return "Job not found. Please use numbers 1-5."

def create_job_agent():
    llm = ChatOpenAI(
        model="gpt-4o-mini", 
        temperature=0,
        api_key=settings.openai_api_key
    )
    
    tools = [get_job_count, get_job_info]
    
    agent = create_agent(
        llm,
        tools,
        system_prompt="You are a helpful job search assistant. Use your tools to answer questions."
    )
    
    return agent