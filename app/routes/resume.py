from fastapi import APIRouter, UploadFile, File, HTTPException, status
import pdfplumber
import io

router = APIRouter()

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)) -> str:
    # validate file
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only pdf files are allowed")

    try:
        file_content = await file.read()
        response = read_pdf_plumber(file_content)
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error while reading pdf: {str(e)}")

def read_pdf_plumber(file_bytes):
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text