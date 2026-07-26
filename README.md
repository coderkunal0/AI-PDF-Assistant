# 🤖 AI PDF Assistant

An AI-powered PDF Assistant built using **RAG (Retrieval-Augmented Generation), LangChain, Ollama, ChromaDB, and Streamlit**.

The application allows users to upload PDF documents and interact with their content using AI. It retrieves relevant information from uploaded PDFs and generates answers based on the document context.

## 🚀 Features

- 📄 Upload one or multiple PDF documents
- 💬 Ask questions directly from PDF content
- 🧠 Retrieval-Augmented Generation (RAG)
- 🔍 Semantic search using vector embeddings
- 📄 AI-powered PDF Summary
- 🎤 Viva Question Generator
- 📝 MCQ Generator
- 📚 Study Notes Generator
- 🎯 Multiple answer modes: Brief, Normal, Detailed (5 Marks), Detailed (10 Marks)
- 👤 Login and Sign-Up system
- 💾 Chat history support
- 🔒 Local AI processing using Ollama
- 🎨 Interactive Streamlit interface

## 🧠 How It Works

1. User uploads one or more PDF files.
2. PDF text is extracted and divided into smaller chunks.
3. Ollama embeddings convert the chunks into vector representations.
4. ChromaDB stores and indexes these vectors.
5. When the user asks a question, relevant chunks are retrieved.
6. The retrieved PDF context is sent to the LLM.
7. The AI generates an answer based on the retrieved document content.

## 🛠️ Tech Stack

- Python
- Streamlit
- LangChain
- Ollama
- Llama 3.2
- Nomic Embed Text
- ChromaDB
- SQLite
- PyPDF

## 📂 Project Structure

```text
AI-PDF-Assistant/
│
├── app.py
├── database.py
├── requirements.txt
├── .gitignore
├── images/
│
├── uploads/        # Generated locally
├── chroma_db/      # Generated locally
├── chat_history/   # Generated locally
└── users.db        # Generated locally
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/coderkunal0/AI-PDF-Assistant.git
cd AI-PDF-Assistant
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Ollama and download the required models:

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

Run the application:

```bash
python -m streamlit run app.py
```

Then open the local Streamlit address shown in the terminal, usually:

```text
http://localhost:8501
```

## 🔐 Privacy

Uploaded PDFs, user database, ChromaDB data, chat history, environment files, and Streamlit secrets are excluded from Git tracking using `.gitignore`.

## 🎯 Use Cases

This project can be useful for:

- Students studying from notes and textbooks
- Viva preparation
- Exam preparation
- PDF question answering
- Document summarization
- Generating MCQs and study notes
- Searching large PDF documents using natural language

## 🔮 Future Improvements

- Cloud deployment
- Improved document management
- Support for DOCX and TXT files
- Better chat-history management
- Source/page citations in AI responses
- Additional LLM support

## 👨‍💻 Author

**Kunal Patil**

B.Tech Data Science  
G H Raisoni College of Engineering and Management, Jalgaon

---

⭐ If you find this project useful, consider starring the repository.
