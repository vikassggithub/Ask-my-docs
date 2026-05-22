"""
Streamlit Frontend for PDF RAG System
"""
import streamlit as st
import requests

# API Configuration
API_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="Ask My Docs - PDF Q&A",
    page_icon="📚",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .answer-box {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "documents_loaded" not in st.session_state:
    st.session_state.documents_loaded = False

# Sidebar
with st.sidebar:
    st.title("📁 Document Manager")
    
    # Check backend connection
    try:
        health = requests.get(f"{API_URL}/health", timeout=2)
        if health.status_code == 200:
            st.success("✅ Backend Connected")
            st.info("🤖 LLM: Groq Llama 3")
    except:
        st.error("❌ Backend not running")
        st.markdown("Start backend: `cd backend && uvicorn server:api --reload`")
    
    st.divider()
    
    # File upload
    uploaded_files = st.file_uploader(
        "Upload PDFs (3+ recommended)",
        type=['pdf'],
        accept_multiple_files=True
    )
    
    if uploaded_files and st.button("🚀 Process PDFs", use_container_width=True):
        with st.spinner(f"Processing {len(uploaded_files)} PDFs..."):
            files = [("files", (f.name, f, "application/pdf")) for f in uploaded_files]
            response = requests.post(f"{API_URL}/upload", files=files)
            
            if response.status_code == 200:
                result = response.json()
                st.session_state.documents_loaded = True
                st.success(f"✅ {result['message']} - {result['num_chunks']} chunks!")
                st.rerun()
            else:
                st.error(f"Error: {response.text}")
    
    # Clear button
    if st.session_state.documents_loaded:
        if st.button("🗑️ Clear All Documents", use_container_width=True):
            requests.delete(f"{API_URL}/clear")
            st.session_state.documents_loaded = False
            st.success("All documents cleared!")
            st.rerun()

# Main content
st.markdown("""
<div class="main-header">
    <h1 style="margin:0">📚 Ask My Docs</h1>
    <p style="margin:0; opacity:0.9">RAG-powered PDF Q&A with Groq Llama 3</p>
</div>
""", unsafe_allow_html=True)

# Question input
question = st.text_input(
    "💬 Ask a question about your documents:",
    placeholder="E.g., What are the main findings?"
)

col1, col2 = st.columns([1, 4])
with col1:
    top_k = st.selectbox("📊 Context chunks", [3, 4, 5], index=2)
with col2:
    ask_button = st.button("🔍 Get Answer", use_container_width=True, type="primary")

# Answer generation
if ask_button:
    if not st.session_state.documents_loaded:
        st.warning("⚠️ Please upload and process PDFs first!")
    elif not question.strip():
        st.warning("⚠️ Please enter a question!")
    else:
        with st.spinner("🔍 Generating answer with Groq Llama 3..."):
            try:
                response = requests.post(
                    f"{API_URL}/ask",
                    json={"question": question, "top_k": top_k}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display answer
                    st.markdown("### 🤖 Answer")
                    st.markdown(f'<div class="answer-box">{result["answer"]}</div>', unsafe_allow_html=True)
                    
                    # Display sources
                    if result["sources"]:
                        st.markdown("### 📖 Sources")
                        for idx, source in enumerate(result["sources"], 1):
                            with st.expander(f"Source {idx}: {source['metadata']['filename']} (Page {source['metadata']['page']})"):
                                st.text(source["text"][:400])
                    else:
                        st.info("No sources found.")
                else:
                    st.error(f"Error: {response.text}")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.divider()
st.caption("Powered by Groq Llama 3 | ChromaDB | FastAPI | Streamlit")