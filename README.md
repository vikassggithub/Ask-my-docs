Candidate Information

Name : Vikas S G
Email :vikassg8888@gmail.com
Phone  : +91 8105013157
Role Applied For : AI Developer

====================================================================================================

Project Overview:

Ask My Docs is a production-ready Retrieval-Augmented Generation (RAG) system that allows users to upload PDF documents and ask natural language questions about their content. The application retrieves the most relevant chunks from the documents and generates accurate answers using Groq's Llama 3.3 70B model.

What I Built:

* PDF Ingestion Engine: Extracts text from uploaded PDFs and splits into 800-character chunks with 200-character overlap
* Vector Search System: Uses sentence-transformers (all-MiniLM-L6-v2) for local embeddings and ChromaDB for similarity search
* Question Answering API: FastAPI backend that retrieves relevant chunks and sends them to Groq's LLM
* Web Interface: Streamlit-based UI for easy document upload and questioning
* Source Tracking: Every answer includes the source filename and page number
* Safety Mechanism: Built-in "I don't know" prompt prevents hallucination when context is insufficient

=========================================================================================================

Technology Stack:

| Category        | Technology            | Version | Purpose                               |
| --------------- | --------------------- | ------- | ------------------------------------- |
| Frontend        | Streamlit             | 1.31.0  | Web UI for file upload and Q&A        |
| Backend         | FastAPI               | 0.104.1 | REST API server                       |
| Vector Database | ChromaDB              | 0.4.22  | Store and search document embeddings  |
| Embeddings      | sentence-transformers | 2.2.2   | Convert text to vectors (local, free) |
| Embedding Model | all-MiniLM-L6-v2      | -       | 384-dimension embeddings              |
| LLM API         | Groq                  | 0.4.2   | Llama 3.3 70B (free tier)             |
| PDF Processing  | PyPDF                 | 3.17.4  | Extract text from PDFs                |
| Text Splitting  | Custom                | -       | 800 char chunks, 200 overlap          |
| Language        | Python                | 3.10+   | Core programming language             |

=====================================================================================================

Setup and Installation Instructions:

Prerequisites:

| Requirement | Version | Check Command             |
| ----------- | ------- | ------------------------- |
| Python      | 3.10+   | `python --version`        |
| pip         | Latest  | `python -m pip --version` |
| Git         | Latest  | `git --version`           |

Step 1: Clone the Repository

```bash
git clone https://github.com/vikassggithub/Ask-my-docs.git
cd Ask-my-docs
```

Step 2: Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

Step 3: Install Backend Dependencies

```bash
cd backend
python -m pip install -r requirements.txt
cd ..
```

Step 4: Install Frontend Dependencies

```bash
cd frontend
python -m pip install -r requirements.txt
cd ..
```

Configuration

Environment Variables

Create a .env file in the root directory:

Windows:

```bash
echo GROQ_API_KEY=your_groq_api_key_here > .env
```

* Sign up with Google or Email
* Click API Keys → Create API Key
* Name it ask-my-docs
* Copy the key (starts with gsk_)
* Add to .env file

Important: Never commit .env to GitHub. Use .env.example as template.

.env.example (Commit this to GitHub)

```env
GROQ_API_KEY=your_groq_api_key_here
LLM_PROVIDER=groq
```

Running the Project Locally:

Terminal 1 - Start Backend

```bash
cd backend
python -m uvicorn server:api --reload --port 8000
```

Expected output:

```text
INFO: Uvicorn running on http://127.0.0.1:8000
RAG Engine initialized with Groq Llama 3
```

Terminal 2 - Start Frontend (Open new terminal)

```bash
cd frontend
streamlit run main.py
```

Expected output:

```text
You can now view your Streamlit app at:
Local URL: http://localhost:8501
```

Open Browser

Navigate to: [http://localhost:8501](http://localhost:8501)

=================================================================================================

Live Deployment

Currently running locally only. See demo recording for full functionality.

Known Issues and Limitations

| Issue                        | Impact             | Workaround                |
| ---------------------------- | ------------------ | ------------------------- |
| Complex PDF tables           | Data loss possible | Use text-heavy PDFs       |
| Scanned PDFs (images)        | No text extraction | Need OCR preprocessing    |
| Very large PDFs (500+ pages) | Slower processing  | Works but takes time      |
| Non-English text             | Reduced accuracy   | English-optimized model   |
| Free API rate limits         | 30 requests/minute | Wait or use multiple keys |

Assumptions Made

* PDFs are text-based (not scanned images)
* Stable internet connection for Groq API
* Python 3.10+ installed
* Documents are in English

=======================================================================================================

Sample Q&A Results

Test Documents Used

| # | Document Name      | Size  | Content Type                                |
| - | ------------------ | ----- | ------------------------------------------- |
| 1 | SADP Notes.pdf     | 4.8MB | Design Patterns, MVC, Software Architecture |
| 2 | SQLNotes-1.pdf     | 3.0MB | SQL Database concepts, queries              |
| 3 | StringPrograms.pdf | 54KB  | String manipulation programs in Python      |

Example 1: String Reversal Program

User Question:
can you give String Reversal program

AI Answer:
The String Reversal program is given in two functions: stringrevincre(s1) and stringrevdecre(s1). Here is the code:

```python
def stringrevincre(s1):
    nstr = ""
    for i in range(0, len(s1)):
        nstr = s1[i] + nstr
    return nstr

def stringrevdecre(s1):
    nstr = ""
    for i in range(len(s1)-1, -1, -1):
        nstr = nstr + s1[i]
    return nstr
```

Source: StringPrograms.pdf
Relevance Score: 0.89

Example 2: SQL SELECT Statement

User Question:
What is a SELECT statement in SQL?

AI Answer:
The SELECT statement is used to select data from a database. The data returned is stored in a result table, called the result-set.

Basic syntax:

```sql
SELECT column1, column2 FROM table_name;
SELECT * FROM table_name;
```

The SELECT DISTINCT statement is used to return only distinct (different) values.

Source: SQLNotes-1.pdf
Relevance Score: 0.92

Example 3: Design Pattern Definition

User Question:
What is a Design Pattern?

AI Answer:
A design pattern describes a problem which occurs over and over again in our environment, and then describes the core of the solution to that problem, in such a way that you can use this solution a million times over, without ever doing it the same way twice.

In general, a pattern has four essential elements:

* Pattern Name: A handle to describe the design problem
* Problem: When to apply the pattern
* Solution: The elements that make up the design
* Consequences: Results and trade-offs of applying the pattern

Source: SADP Notes.pdf, Page 1
Relevance Score: 0.95

Example 4: Types of Design Patterns

User Question:
What are the categories of design patterns?

AI Answer:
Design patterns are classified into three categories based on purpose:

Creational Patterns (Object Creation):
Abstract Factory, Builder, Prototype, Singleton

Structural Patterns (Class/Object Composition):
Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy

Behavioral Patterns (Interaction & Responsibility):
Chain of Responsibility, Command, Interpreter, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor

Source: SADP Notes.pdf, Page 6
Relevance Score: 0.88

Example 5: Outside Document Context (Correct Refusal)

User Question:
What is the capital of France?

AI Answer:
I don't know based on the provided documents. The uploaded PDFs contain information about design patterns, SQL queries, and string programs, but no information about world capitals or geography.

Source: No relevant sources found
Relevance Score: N/A (Correct refusal to hallucinate)

======================================================================================================

Performance Summary:

| Metric                        | Value       |
| ----------------------------- | ----------- |
| Total Documents Tested        | 3 PDFs      |
| Total Questions Asked         | 5           |
| Relevant Answers              | 4           |
| Correct Refusals              | 1           |
| Average Response Time         | 2-4 seconds |
| Accuracy (relevant questions) | 100%        |
| Source Tracking Accuracy      | 100%        |
| Hallucination Prevention      | 100%        |

======================================================================================================

What Worked Well:

* Accurate retrieval of code snippets (String reversal program)
* Correct SQL syntax extraction
* Page-level source tracking for design patterns
* Perfect "I don't know" response for out-of-context questions
* Fast response time (2-4 seconds per query)

=========================================================================================================

Mandatory Features

| Feature                                |
| -------------------------------------- |
| PDF Ingestion                          |
| Text Chunking (800 chars, 200 overlap) |
| sentence-transformers embeddings       |
| ChromaDB vector store                  |
| Groq LLM API (free tier)               |
| Top 3-5 chunks retrieval               |
| Display answer                         |
| Display source chunks                  |
| Streamlit UI                           |
| Sample Q&A in README                   |

==============================================================================================

Bonus Features:

* LangChain Integration
* Page Number Citations
* Cache Embeddings
* "I don't know" Prompt
* Multi-turn Conversation

=============================================================================================================

Limitations Noticed:

* Code formatting could be better with proper syntax highlighting
* Very large PDFs (50+ pages) take longer to process
* Free API has 30 requests/minute limit

====================================================================================================

Demo Recording:

Link:"[https://drive.google.com/file/d/1x9eN6eAOwq7aJwKDh9gE01TwdKqeGnBG/view?usp=sharing](https://drive.google.com/file/d/1x9eN6eAOwq7aJwKDh9gE01TwdKqeGnBG/view?usp=sharing)"







