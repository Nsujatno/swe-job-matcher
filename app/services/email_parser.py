import re
from typing import List, Dict, Optional


def parse_swelist_email(email_text: str) -> List[Dict[str, str]]:
    jobs = []
    
    lines = email_text.strip().split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines and common email headers/footers
        if not line or _should_skip_line(line):
            i += 1
            continue
        
        # Match pattern: "Company: Job Title"
        # Handles companies with spaces, hyphens, special chars
        match = re.match(r'^(.+?):\s*(.+)$', line)
        
        if match:
            company = match.group(1).strip()
            title = match.group(2).strip()

            jobs.append({
                "company": company,
                "title": title,
            })
        
        i += 1
    
    return jobs


def _should_skip_line(line: str) -> bool:
    skip_patterns = [
        r'^Hey\s+\w+!',  # Email greeting
        r'^Here is your daily update',  # Header text
        r'built SWElist',  # Description
        r'forward it to a friend',  # CTA
        r'shoutout to',  # Shoutout section
        r'Link to Simplify',  # Simplify link
        r'See more details',  # Footer
        r'Click here to Unsubscribe',  # Unsubscribe
        r'Summer\d{4}-Internships',  # Repo link
        r'^\s*$',  # Empty lines
    ]
    
    for pattern in skip_patterns:
        if re.search(pattern, line, re.IGNORECASE):
            return True
    
    return False


def extract_job_count(jobs: List[Dict[str, str]]) -> Dict[str, int]:
    companies = set(job['company'] for job in jobs)
    
    return {
        "total_jobs": len(jobs),
        "unique_companies": len(companies)
    }