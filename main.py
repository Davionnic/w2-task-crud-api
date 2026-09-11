from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="Task API",
    description="A simple CRUD API for managing tasks",
    version="1.0"
)

@app.get("/")
def root():
    """Root endpoint returning API information"""
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)