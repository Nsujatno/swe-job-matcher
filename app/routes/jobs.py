from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict
from app.services.email_parser import parse_swelist_email, extract_job_count
from app.models import ParseEmailRequest, ParseEmailResponse

router = APIRouter()

@router.post("/jobs/parse-email", response_model=ParseEmailResponse)
async def parse_email(request: ParseEmailRequest):
    if not request.email_text or not request.email_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email text cannot be empty"
        )
    
    try:
        # Parse email to extract job links
        jobs = parse_swelist_email(request.email_text)
        
        if not jobs:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No job postings found in email text"
            )
        
        # Get statistics
        stats = extract_job_count(jobs)
        
        return ParseEmailResponse(
            jobs=jobs,
            count=stats["total_jobs"],
            unique_companies=stats["unique_companies"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error parsing email: {str(e)}"
        )