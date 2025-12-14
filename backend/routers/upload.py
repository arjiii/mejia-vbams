from fastapi import APIRouter, File, UploadFile, HTTPException
import shutil
import os
import uuid
from typing import List

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def upload_files(files: List[UploadFile] = File(...)):
    uploaded_urls = []
    
    for file in files:
        try:
            # Generate unique filename
            file_ext = os.path.splitext(file.filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_ext}"
            file_path = os.path.join(UPLOAD_DIR, unique_filename)
            
            # Save file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
                
            # Construct URL (assuming simple static serving setup or relative path)
            # For now, return relative path that frontend can use or backend can serve
            # In production, this would be an S3 URL
            file_url = f"/static/uploads/{unique_filename}"
            uploaded_urls.append(file_url)
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload {file.filename}: {str(e)}")
            
    return {"urls": uploaded_urls}
