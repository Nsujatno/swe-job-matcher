import uuid
from fastapi import APIRouter, HTTPException, status
from openai import OpenAI
from app.config import settings, chroma_client
from app.models import ResumeUploadRequest

router = APIRouter()
client = OpenAI(api_key=settings.openai_api_key)

@router.post("/resume")
async def upload_resume(request: ResumeUploadRequest):
    resume_id = str(uuid.uuid4())

    chunks = []
    chunk_metadata = []
    chunk_ids = []

    chunks.append(request.resume.text)
    chunk_metadata.append({
        "resume_id": resume_id,
        "chunk_type": "full_text",
        "roles": ",".join(request.preferences.role),
        "experience_level": request.preferences.experience_level
    })
    chunk_ids.append(f"{resume_id}_full")

    # sills as separate chunk
    if request.resume.skills:
        skills_text = "Skills: " + ", ".join(request.resume.skills)
        chunks.append(skills_text)
        chunk_metadata.append({
            "resume_id": resume_id,
            "chunk_type": "skills",
            "roles": ",".join(request.preferences.role),
            "experience_level": request.preferences.experience_level
        })
        chunk_ids.append(f"{resume_id}_skills")

    # each experience as a separate chunk
    if request.resume.experience:
        for i, exp in enumerate(request.resume.experience):
            chunks.append(f"Experience: {exp}")
            chunk_metadata.append({
                "resume_id": resume_id,
                "chunk_type": "experience",
                "experience_index": i,
                "roles": ",".join(request.preferences.role),
                "experience_level": request.preferences.experience_level
            })
            chunk_ids.append(f"{resume_id}_exp_{i}")
            
    # each project as a separate chunk
    if request.resume.projects:
        for i, proj in enumerate(request.resume.projects):
            chunks.append(f"Project: {proj}")
            chunk_metadata.append({
                "resume_id": resume_id,
                "chunk_type": "project",
                "project_index": i,
                "roles": ",".join(request.preferences.role),
                "experience_level": request.preferences.experience_level
            })
            chunk_ids.append(f"{resume_id}_proj_{i}")
    
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=chunks
        )

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating embeddings for resume {str(e)}")
    
    try:
        collection = chroma_client.get_or_create_collection(name="resumes")
        embeddings = [item.embedding for item in response.data]

        # Store all chunks in ChromaDB
        collection.add(
            embeddings=embeddings,
            documents=chunks,
            ids=chunk_ids,
            metadatas=chunk_metadata
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error storing resume embeddings into db {str(e)}")
    
    
    return {
        "resume_id": resume_id,
        "chunks_stored": len(chunks)
    }