from fastapi import FastAPI, UploadFile, File, HTTPException
from app.services.parser import extract_text_from_pdf, extract_text_from_docx

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

    return {
        "filename": file.filename,
        "characters": len(text),
        "preview": text[:500],
    }