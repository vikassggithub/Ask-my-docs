"""
FastAPI Backend for PDF RAG System
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import tempfile
import os
from rag_engine import GroqRAGEngine

# Create FastAPI instance
api = FastAPI(title="PDF RAG API", description="Ask questions about your PDFs")

# Enable CORS for Streamlit frontend
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG engine
rag_engine = None

class Question(BaseModel):
    question: str
    top_k: Optional[int] = 5

class AnswerResponse(BaseModel):
    answer: str
    sources: List[dict]
    model_used: str

@api.on_event("startup")
async def startup_event():
    global rag_engine
    try:
        rag_engine = GroqRAGEngine()
        print("✅ RAG Engine initialized with Groq Llama 3")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")

@api.get("/")
async def root():
    return {"message": "PDF RAG API is running", "status": "active", "llm": "Groq Llama 3"}

@api.post("/upload")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    """Upload and process PDFs"""
    if not rag_engine:
        raise HTTPException(status_code=500, detail="RAG Engine not initialized")
    
    temp_dir = tempfile.mkdtemp()
    pdf_paths = []
    filenames = []
    
    try:
        for file in files:
            if not file.filename.endswith('.pdf'):
                raise HTTPException(status_code=400, detail=f"{file.filename} is not a PDF")
            
            temp_path = os.path.join(temp_dir, file.filename)
            with open(temp_path, "wb") as f:
                content = await file.read()
                f.write(content)
            
            pdf_paths.append(temp_path)
            filenames.append(file.filename)
        
        # Add to vector store
        num_chunks = rag_engine.add_pdfs(pdf_paths, filenames)
        
        return {
            "message": f"Successfully processed {len(files)} PDFs",
            "num_chunks": num_chunks,
            "files": filenames
        }
    
    finally:
        for path in pdf_paths:
            if os.path.exists(path):
                os.remove(path)
        os.rmdir(temp_dir)

@api.post("/ask", response_model=AnswerResponse)
async def ask_question(question: Question):
    """Ask a question about uploaded PDFs"""
    if not rag_engine:
        raise HTTPException(status_code=500, detail="RAG Engine not initialized")
    
    result = rag_engine.query(question.question, question.top_k)
    
    return AnswerResponse(
        answer=result["answer"],
        sources=result["sources"],
        model_used=result["model_used"]
    )

@api.delete("/clear")
async def clear_documents():
    """Clear all uploaded documents"""
    if not rag_engine:
        raise HTTPException(status_code=500, detail="RAG Engine not initialized")
    
    rag_engine.clear_all()
    return {"message": "All documents cleared"}

@api.get("/health")
async def health_check():
    return {"status": "healthy", "rag_engine": rag_engine is not None}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api, host="0.0.0.0", port=8000)