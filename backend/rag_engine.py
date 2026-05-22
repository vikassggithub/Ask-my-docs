"""
RAG Engine with Groq API (Llama 3) and ChromaDB
"""
import os
import hashlib
from typing import List, Dict
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class GroqRAGEngine:
    def __init__(self, persist_directory: str = "./chroma_db"):
        # Initialize embedding model (local, free)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        self._setup_collection()
        
        # Initialize Groq client with Llama 3
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        self.groq_client = Groq(api_key=api_key)
        self.llm_model = "llama-3.3-70b-versatile"
        
        # Text splitter settings
        self.chunk_size = 800
        self.chunk_overlap = 200
        
    def _setup_collection(self):
        try:
            self.collection = self.chroma_client.get_collection("pdf_docs")
        except:
            self.collection = self.chroma_client.create_collection(
                name="pdf_docs",
                metadata={"hnsw:space": "cosine"}
            )
    
    def extract_text_from_pdf(self, pdf_path: str) -> List[Dict]:
        reader = PdfReader(pdf_path)
        pages_data = []
        
        for page_num, page in enumerate(reader.pages, 1):
            text = page.extract_text()
            if text.strip():
                chunks = self._split_text(text)
                for chunk_id, chunk in enumerate(chunks):
                    pages_data.append({
                        "text": chunk,
                        "page": page_num,
                        "chunk_id": chunk_id
                    })
        return pages_data
    
    def _split_text(self, text: str) -> List[str]:
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = min(start + self.chunk_size, text_length)
            if end < text_length:
                last_period = text.rfind('.', start, end)
                last_newline = text.rfind('\n', start, end)
                end = max(last_period, last_newline, end)
                if end <= start:
                    end = min(start + self.chunk_size, text_length)
            
            chunks.append(text[start:end].strip())
            start = end - self.chunk_overlap if end < text_length else text_length
        
        return chunks
    
    def get_embedding(self, text: str) -> List[float]:
        return self.embedding_model.encode(text).tolist()
    
    def add_pdfs(self, pdf_paths: List[str], filenames: List[str]) -> int:
        all_chunks = []
        all_embeddings = []
        all_metadatas = []
        all_ids = []
        
        for pdf_path, filename in zip(pdf_paths, filenames):
            pages_data = self.extract_text_from_pdf(pdf_path)
            
            for page_data in pages_data:
                chunk_text = page_data["text"]
                chunk_id = f"{filename}_p{page_data['page']}_c{page_data['chunk_id']}"
                
                all_chunks.append(chunk_text)
                all_metadatas.append({
                    "filename": filename,
                    "page": page_data["page"],
                    "chunk_id": page_data["chunk_id"]
                })
                all_ids.append(chunk_id)
        
        for chunk in all_chunks:
            embedding = self.get_embedding(chunk)
            all_embeddings.append(embedding)
        
        if all_chunks:
            self.collection.add(
                embeddings=all_embeddings,
                documents=all_chunks,
                metadatas=all_metadatas,
                ids=all_ids
            )
        
        return len(all_chunks)
    
    def retrieve_context(self, query: str, top_k: int = 5) -> List[Dict]:
        query_embedding = self.get_embedding(query)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )
        
        contexts = []
        if results['documents'] and results['documents'][0]:
            for i in range(len(results['documents'][0])):
                contexts.append({
                    "text": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "relevance_score": 1 - results['distances'][0][i]
                })
        
        return contexts
    
    def generate_answer(self, query: str, contexts: List[Dict]) -> Dict:
        if not contexts:
            return {
                "answer": "No relevant documents found. Please upload PDFs first.",
                "sources": []
            }
        
        context_text = "\n\n---\n\n".join([
            f"[SOURCE: {ctx['metadata']['filename']}, Page {ctx['metadata']['page']}]\n{ctx['text']}"
            for ctx in contexts
        ])
        
        system_prompt = """You are a helpful assistant that answers questions based ONLY on the provided context. 
Rules:
1. ONLY use information from the context
2. If the answer is not in the context, say "I don't know based on the provided documents"
3. Do NOT make up or hallucinate any information
4. Cite the source filename and page number when giving answers
5. Be concise but complete"""
        
        user_prompt = f"""Context from documents:
{context_text}

Question: {query}

Answer based ONLY on the above context:"""
        
        response = self.groq_client.chat.completions.create(
            model=self.llm_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        return {
            "answer": response.choices[0].message.content,
            "sources": contexts,
            "model_used": self.llm_model
        }
    
    def query(self, question: str, top_k: int = 5) -> Dict:
        contexts = self.retrieve_context(question, top_k)
        return self.generate_answer(question, contexts)
    
    def clear_all(self):
        self.chroma_client.delete_collection("pdf_docs")
        self._setup_collection()