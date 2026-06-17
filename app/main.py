from fastapi import FastAPI, UploadFile, File, HTTPException
from app.services.parser import (
    extract_text_from_pdf,
    extract_text_from_docx,
    split_into_sections,
)
from app.services.skills import extract_skills

app = FastAPI(title="PathForge")


@app.get("/")
def root():
    return {"message": "PathForge is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    file_bytes = await file.read()
    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(file_bytes)
    elif filename.endswith(".docx"):
        text = extract_text_from_docx(file_bytes)
    else:
        raise HTTPException(status_code=400, detail="Please upload a PDF or DOCX file.")

    sections = split_into_sections(text)
    skills = extract_skills(text)

    return {
        "filename": file.filename,
        "characters": len(text),
        "skills": skills,
        "sections": sections,
    }