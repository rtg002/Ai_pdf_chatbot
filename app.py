import streamlit as st
import fitz  # PyMuPDF
import os
from openai import OpenAI

# Set your OpenAI API key
api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# ----------- FUNCTIONS ------------

# Read text from PDF
def read_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Summarize the document using GPT
def summarize_text(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Summarize this text in simple bullet points:\n{text[:3000]}"}
        ],
        temperature=0.5
    )
    return response.choices[0].message.content

# Ask questions about the document using GPT
def ask_gpt_question(text, question):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant helping answer questions about documents."},
            {"role": "user", "content": f"Document:\n{text[:3000]}"},
            {"role": "user", "content": f"Question: {question}"}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

# ----------- STREAMLIT UI ------------

st.title("📄 AI PDF Summarizer + Chatbot (OpenAI GPT)")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Reading PDF..."):
        full_text = read_pdf(uploaded_file)
        st.success("PDF loaded!")

    if st.button("Generate Summary"):
        with st.spinner("Summarizing..."):
            summary = summarize_text(full_text)
            st.subheader("📌 Summary:")
            st.write(summary)

    question = st.text_input("💬 Ask a question about the document:")
    if question:
        with st.spinner("Answering..."):
            answer = ask_gpt_question(full_text, question)
            st.subheader("📖 Answer:")
            st.write(answer)
