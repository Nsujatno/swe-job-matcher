import requests
import re
from rapidfuzz import fuzz
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from bs4 import BeautifulSoup
from app.config import settings

GITHUB_RAW_URL = "https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/dev/README.md"

@tool(description="Scrapes the first 10 job postings from the Summer2026-Internships GitHub README. Returns a list of dicts: {company, title, link}")
def get_first_10_github_jobs() -> list:
    try:
        response = requests.get(GITHUB_RAW_URL, timeout=30)
        response.raise_for_status()
        md = response.text
    except Exception as e:
        return [{"error": f"Could not fetch README: {e}"}]
    
    soup = BeautifulSoup(md, 'html.parser')
    
    # find the software engineering section
    table = soup.find('table')
    if not table:
        return [{"error": "No table found in README"}]
    
    jobs = []
    
    # Find all rows in tbody
    tbody = table.find('tbody')
    if not tbody:
        return [{"error": "No tbody found in table"}]
    
    rows = tbody.find_all('tr')
    
    for row in rows[:10]:
        cells = row.find_all('td')
        
        if len(cells) < 4:
            continue
        
        # Extract company (cell 0)
        company_cell = cells[0]
        company = company_cell.get_text(strip=True)
        
        # Clean up company name (remove extra symbols)
        company = company.replace('↳', '').strip()
        
        # Skip empty or continuation rows
        if not company or company == '':
            continue
        
        # Extract title (cell 1)
        title = cells[1].get_text(strip=True)
        
        # Extract location (cell 2)
        location = cells[2].get_text(strip=True)
        
        # Extract application link (cell 3)
        app_cell = cells[3]
        link_tag = app_cell.find('a', href=True)
        link = link_tag['href'] if link_tag else None
        
        jobs.append({
            "company": company,
            "title": title,
            "location": location,
            "link": link
        })
        
        if len(jobs) >= 10:
            break
    
    return jobs       



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
    
    tools = [get_job_count, get_job_info, find_github_job_link]
    
    agent = create_agent(
        llm,
        tools,
        system_prompt="You are a helpful job search assistant. Use your tools to answer questions."
    )
    
    return agent