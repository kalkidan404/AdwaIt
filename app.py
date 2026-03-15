import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Free LangChain imports

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_classic.chains import RetrievalQA

load_dotenv()

app = FastAPI(title="Adwa AI Assistant (Free Version)")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, or list your streamlit URL specifically
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -----------------------------

# 1. LOAD WEBSITE DATA

# -----------------------------

urls = [
"https://en.wikipedia.org/wiki/Battle_of_Adwa",
"https://en.wikipedia.org/wiki/Menelik_II",
"https://en.wikipedia.org/wiki/Taytu_Betul"
]

loader = WebBaseLoader(urls)
docs = loader.load()

# -----------------------------

# 2. TEXT CHUNKING

# -----------------------------

splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=150)
documents = splitter.split_documents(docs)

# -----------------------------

# 3. VECTOR DATABASE

# -----------------------------

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vectorstore = FAISS.from_documents(documents, embeddings)
retriever = vectorstore.as_retriever()

# -----------------------------

# 4. LLM (Groq)

# -----------------------------

llm = ChatGroq(
model_name="llama-3.1-8b-instant",
temperature=0,
groq_api_key=os.getenv("GROQ_API_KEY")
)

qa_chain = RetrievalQA.from_chain_type(
llm=llm,
retriever=retriever,
chain_type="stuff"
)

# -----------------------------

# API SCHEMA

# -----------------------------

class Question(BaseModel):
 question: str

# -----------------------------

# ASK ENDPOINT

# -----------------------------

@app.post("/ask")
async def ask_question(q: Question):

    question = q.question.lower()

    allowed_keywords = [
        "adwa","menelik","taytu","ethiopia",
        "italy","italian","battle","wuchale",
        "ras","makonnen","alula"
    ]

    if not any(word in question for word in allowed_keywords):
        return {
            "question": q.question,
            "answer": "I can only answer questions related to the Battle of Adwa and the Ethiopian–Italian conflict."
        }

    formatted_question = f"""
You are a historian specializing in the Battle of Adwa.

Answer the question clearly using historical facts.

Question: {q.question}
"""

    response = qa_chain.invoke(formatted_question)

    return {
        "question": q.question,
        "answer": response["result"]
    }