from fastapi import FastAPI

app = FastAPI(title="PathForge")

@app.get("/")
def root():
    return {"message": "PathForge is running"}

@app.get("/health")
def health():
    return {"status": "ok"}