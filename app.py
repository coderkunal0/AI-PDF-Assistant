import streamlit as st
import os
import uuid

from database import register, login

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI PDF Assistant",
    page_icon="🤖",
    layout="wide"
)


# =====================================================
# FOLDERS
# =====================================================

os.makedirs("uploads", exist_ok=True)
os.makedirs("chroma_db", exist_ok=True)
os.makedirs("chat_history", exist_ok=True)


# =====================================================
# SESSION STATE
# =====================================================

if "login" not in st.session_state:
    st.session_state.login = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "chat" not in st.session_state:
    st.session_state.chat = []

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "processed_files" not in st.session_state:
    st.session_state.processed_files = []

if "chat_id" not in st.session_state:
    st.session_state.chat_id = str(uuid.uuid4())


# =====================================================
# AI MODELS
# =====================================================

embedding = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# =====================================================
# CHAT HISTORY FUNCTIONS
# =====================================================

import json

def save_chat():

    if not st.session_state.chat:
        return

    file_path = os.path.join(
        "chat_history",
        f"{st.session_state.chat_id}.json"
    )

    data = {

        "chat_id": st.session_state.chat_id,

        "messages": st.session_state.chat

    }

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


def get_chat_files():

    os.makedirs(
        "chat_history",
        exist_ok=True
    )

    files = [

        f for f in os.listdir("chat_history")

        if f.endswith(".json")

    ]

    files.sort(reverse=True)

    return files


def load_chat(file_name):

    file_path = os.path.join(
        "chat_history",
        file_name
    )

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    st.session_state.chat = data["messages"]

    st.session_state.chat_id = data["chat_id"]
# =====================================================
# EXPORT CHAT FUNCTION
# =====================================================

def export_chat():

    if not st.session_state.chat:
        return ""

    text = ""

    for msg in st.session_state.chat:

        role = msg["role"].upper()

        text += f"{role}\n"

        text += msg["content"]

        text += "\n\n"

    return text
# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

.stApp{
    background-image:url("https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1920");
    background-size:cover;
    background-position:center;
    background-attachment:fixed;
}

.block-container{
    background:rgba(0,0,0,0.80);
    border-radius:15px;
    padding:20px;
}

h1,h2,h3,h4,h5,h6,p,label,span{
    color:white !important;
}

[data-testid="stSidebar"]{
    background:#111827;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# LOGIN PAGE
# =====================================================

if not st.session_state.login:

    c1, c2, c3 = st.columns([1,2,1])

    with c2:

        st.image("images/raisone.jpg", width=180)

        st.title("🤖 AI PDF Assistant")

        st.write("Chat with your PDF using AI")

        option = st.radio(
            "Select",
            ["Login", "Sign Up"],
            horizontal=True
        )

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if option == "Sign Up":

            if st.button("Create Account"):

                if register(username, password):

                    st.success("Account Created Successfully")

                else:

                    st.error("Username already exists")

        else:

            if st.button("Login"):

                if login(username, password):

                    st.session_state.login = True
                    st.session_state.username = username

                    st.rerun()

                else:

                    st.error("Invalid Username or Password")

    st.stop()
    # =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("🤖 AI PDF Assistant")

    st.success(f"👋 Welcome {st.session_state.username}")

    st.markdown("---")

    if st.button("➕ New Chat", use_container_width=True):
        save_chat()
        st.session_state.chat = []
        st.session_state.chat_id = str(uuid.uuid4())

        st.rerun()

    st.markdown("---")

    uploaded_files = st.file_uploader(
        "📂 Upload PDF(s)",
        type=["pdf"],
        accept_multiple_files=True
    )

    st.markdown("---")

    st.subheader("💬 Recent Chats")

    history_files = get_chat_files()

    if not history_files:

        st.info("No Chats Yet")

    else:

     for file in history_files[:10]:

        chat_name = file.replace(".json", "")

        if st.button(

            f"💬 {chat_name[:8]}...",

            key=f"history_{file}",

            use_container_width=True

        ):

            load_chat(file)

            st.rerun()

    st.markdown("---")

    st.subheader("🛠 AI Tools")

    summary_btn = st.button(
        "📄 PDF Summary",
        use_container_width=True
    )

    viva_btn = st.button(
        "🎤 Viva Questions",
        use_container_width=True
    )

    mcq_btn = st.button(
        "📝 MCQ Generator",
        use_container_width=True
    )

    notes_btn = st.button(
        "📚 Study Notes",
        use_container_width=True
    )
    st.markdown("---")

    st.download_button(
    "💾 Export Chat",
    data=export_chat(),
    file_name="AI_PDF_Chat.txt",
    mime="text/plain",
    use_container_width=True
)

    st.markdown("---")

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.login = False
        st.session_state.username = ""
        st.session_state.chat = []
        st.session_state.retriever = None

        st.rerun()
        # =====================================================
# MAIN PAGE
# =====================================================

st.title("📄 Chat With Your PDF")

st.info("Upload one or more PDF files from the sidebar to get started.")
# =====================================================
# PDF UPLOAD
# =====================================================



uploaded_files = st.file_uploader(
    "Upload PDF(s)",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:

    current_files = sorted([file.name for file in uploaded_files])

    if current_files != st.session_state.processed_files:

        with st.spinner("📚 Processing PDF(s)..."):

            all_documents = []

            for uploaded_file in uploaded_files:

                pdf_path = os.path.join(
                    "uploads",
                    uploaded_file.name
                )

                with open(pdf_path, "wb") as f:

                    f.write(
                        uploaded_file.getbuffer()
                    )

                loader = PyPDFLoader(pdf_path)

                documents = loader.load()

                all_documents.extend(documents)

            splitter = RecursiveCharacterTextSplitter(

                chunk_size=1000,

                chunk_overlap=200

            )

            docs = splitter.split_documents(
                all_documents
            )

            vectorstore = Chroma.from_documents(

                documents=docs,

                embedding=embedding,

                persist_directory="chroma_db"

            )

            st.session_state.retriever = vectorstore.as_retriever(

                search_kwargs={
                    "k":10
                }

            )

            st.session_state.processed_files = current_files

        st.success("✅ PDF Ready!")

else:

    st.info("Upload one or more PDF files from the sidebar.")
    # =====================================================
# =====================================================
# CHAT HISTORY
# =====================================================

for msg in st.session_state.chat:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])


# =====================================================
# ANSWER TYPE
# =====================================================

answer_type = st.selectbox(
    "📝 Answer Type",
    [
        "Brief (2-4 lines)",
        "Normal",
        "Detailed (5 Marks)",
        "Detailed (10 Marks)"
    ]
)


# =====================================================
# CHAT INPUT
# =====================================================

question = st.chat_input(
    "💬 Ask anything about your PDF..."
)

if question:

    if st.session_state.retriever is None:

        st.warning("⚠ Please upload a PDF first.")

    else:

        # Save User Message

        st.session_state.chat.append(
            {
                "role": "user",
                "content": question
            }
        )
        save_chat()

        with st.chat_message("user"):

            st.markdown(question)

        # Search PDF

        docs = st.session_state.retriever.invoke(question)

        context = "\n\n".join(

            [
                f"Page {doc.metadata.get('page',0)+1}\n{doc.page_content}"
                for doc in docs
            ]

        )

        # Answer Style

        instruction = ""

        if answer_type == "Brief (2-4 lines)":

            instruction = """
Give the answer in only 2 to 4 lines.
"""

        elif answer_type == "Normal":

            instruction = """
Give the answer in one or two paragraphs.
"""

        elif answer_type == "Detailed (5 Marks)":

            instruction = """
Write around 300-400 words.

Include:

Definition

Explanation

Features

Advantages

Applications

Conclusion
"""

        else:

            instruction = """
Write around 600-800 words.

Include:

Definition

Introduction

Detailed Explanation

Features

Advantages

Disadvantages

Applications

Conclusion
"""
        # =====================================================
        # PROMPT
        # =====================================================

        prompt = f"""
You are an Expert AI PDF Assistant.

IMPORTANT RULES

1. Answer ONLY from the uploaded PDF.
2. Never use your own knowledge.
3. Never guess.
4. If the answer is not found, reply exactly:

"I couldn't find this information in the uploaded PDF."

----------------------------------

PDF CONTEXT

{context}

----------------------------------

QUESTION

{question}

----------------------------------

ANSWER STYLE

{instruction}

----------------------------------

Generate the best possible answer.
"""

        # =====================================================
        # AI RESPONSE
        # =====================================================

        with st.chat_message("assistant"):

            with st.spinner("🤖 Thinking..."):

                response = llm.invoke(prompt)
                pages = sorted(
    list(
        set(
            [
                doc.metadata.get("page", 0) + 1
                for doc in docs
            ]
        )
    )
)

                answer = response.text

                st.markdown(answer)

        st.session_state.chat.append(
            {
                "role": "assistant",
                "content": answer
            }
        )
        # =====================================================
# PDF SUMMARY
# =====================================================

if summary_btn:

    if st.session_state.retriever is None:

        st.warning("⚠ Please upload a PDF first.")

    else:

        docs = st.session_state.retriever.invoke(
            "Give complete summary of the uploaded PDF."
        )

        context = "\n\n".join(
            [doc.page_content for doc in docs]
        )

        prompt = f"""
You are an AI PDF Assistant.

Read the PDF context carefully and generate a complete summary.

Rules:

- Use only PDF information.
- Never guess.
- Write in simple English.
- Use headings.
- Use bullet points.
- End with a conclusion.

PDF Context:

{context}
"""

        with st.spinner("📄 Generating Summary..."):

            response = llm.invoke(prompt)

        st.subheader("📄 PDF Summary")

        st.markdown(response.content)
        # =====================================================
# MCQ GENERATOR
# =====================================================

if mcq_btn:

    if st.session_state.retriever is None:

        st.warning("⚠ Please upload a PDF first.")

    else:

        docs = st.session_state.retriever.invoke(
            "Generate 10 multiple choice questions from the uploaded PDF."
        )

        context = "\n\n".join(
            [doc.page_content for doc in docs]
        )

        prompt = f"""
You are an AI PDF Assistant.

Using ONLY the PDF context, generate 10 Multiple Choice Questions.

Rules:
- Each question should have 4 options (A, B, C, D)
- Mark the correct answer.
- Do not use outside knowledge.

PDF Context:

{context}
"""

        with st.spinner("📝 Generating MCQs..."):

            response = llm.invoke(prompt)

        st.subheader("📝 MCQ Generator")

        st.markdown(response.content)
        # =====================================================
# VIVA QUESTION GENERATOR
# =====================================================

if viva_btn:

    if st.session_state.retriever is None:

        st.warning("⚠ Please upload a PDF first.")

    else:

        docs = st.session_state.retriever.invoke(
            "Generate viva questions from the uploaded PDF."
        )

        context = "\n\n".join(
            [doc.page_content for doc in docs]
        )

        prompt = f"""
You are an AI PDF Assistant.

Using ONLY the uploaded PDF context, generate 15 viva questions.

Rules:

- Questions only
- No answers
- Start from easy
- End with difficult questions
- Use only PDF information

PDF Context:

{context}
"""

        with st.spinner("🎤 Generating Viva Questions..."):

            response = llm.invoke(prompt)

        st.subheader("🎤 Viva Questions")

        st.markdown(response.content)
        # =====================================================
# STUDY NOTES GENERATOR
# =====================================================

if notes_btn:

    if st.session_state.retriever is None:

        st.warning("⚠ Please upload a PDF first.")

    else:

        docs = st.session_state.retriever.invoke(
            "Create complete study notes from the uploaded PDF."
        )

        context = "\n\n".join(
            [doc.page_content for doc in docs]
        )

        prompt = f"""
You are an AI PDF Assistant.

Create well-structured study notes using ONLY the uploaded PDF.

Rules:

- Use headings
- Use bullet points
- Keep language simple
- Highlight important concepts
- Do not use outside knowledge

PDF Context:

{context}
"""

        with st.spinner("📚 Creating Study Notes..."):

            response = llm.invoke(prompt)

        st.subheader("📚 Study Notes")

        st.markdown(response.content)
