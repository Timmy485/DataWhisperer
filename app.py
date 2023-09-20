import streamlit as st
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import Chroma
from langchain.llms import GooglePalm
import os
import json
from pathlib import Path
# st. set_page_config(layout="wide")
st.markdown(
    """
    <style>
    .appview-container .main .block-container {
        padding-top: 2rem;
        margin: 0;
    }
    .css-usj992 {
    background-color: transparent;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    "<h1 style='text-align: center; padding: 10px;'>DATA WHISPERER</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<h5 style='text-align: center; padding: 2px;'>Unveil Insights From Docs</h5>",
    unsafe_allow_html=True
)
# Sidebar Navigation with header background color
st.sidebar.markdown(
    "<h3 style= padding: 10px;'>Navigation</h3>",
    unsafe_allow_html=True
)
# Use a dropdown menu for feature selection
selected_feature = st.sidebar.selectbox("Select a Feature", (
    "Upload & Analyze Custom Document",
    "Query Existing Documents",
    "Upload Video file"
))
# Main Content with light background color
st.markdown(
    "<div style='background-color: #f9f9f9; padding: 0px;'>",
    unsafe_allow_html=True
)


# configure google palm
path = os.path.dirname(__file__)
json_path = path+'/config.json'
try:
    with open(json_path, 'r') as config_file:
        config_data = json.load(config_file)
    api_key = config_data.get('key')
except FileNotFoundError:
    # If the config.json file is not found, try reading from Streamlit Secrets
    try:
        api_key = st.secrets["PALM_API"]
    except st.secrets.SecretsFileNotFound:
        st.error(
            "Please provide the API key either in a 'config.json' file or as a Streamlit Secret.")
        st.stop()
llm = GooglePalm(google_api_key=api_key)


def load_single_doc(uploaded_file):
    documents = []
    # Save the uploaded file to a temporary location
    temp_file = Path("temp_file." + uploaded_file.name.split(".")[-1])
    temp_file.write_bytes(uploaded_file.read())

    # Check the file type and process accordingly
    if uploaded_file.type == "application/pdf":
        # Process PDF file using PyPDFLoader
        # Pass the file path as a string
        pdf_loader = PyPDFLoader(str(temp_file))
        documents.extend(pdf_loader.load())
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        # Process DOCX file
        docx_loader = Docx2txtLoader(str(temp_file))
        documents.extend(docx_loader.load())
    elif uploaded_file.type == "text/plain":
        # Process TXT file
        text_loader = TextLoader(str(temp_file))
        documents.extend(text_loader.load())

    temp_file.unlink()
    return documents


def split_docs(documents, chunk_size=1000, chunk_overlap=20):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_splitter.split_documents(documents)
    return docs


def store_embeddings_in_chromadb(docs):
    # create embeddings
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # using chromadb as a vector store and storing the docs in it
    db = Chroma.from_documents(docs, embeddings)
    return db


def retrieve_and_answer_question(prompt):
    if prompt:
        matching_docs = db.similarity_search(prompt)

        # Using q&a chain to get the answer for our query
        chain = load_qa_chain(llm, chain_type="stuff")
        answer = chain.run(input_documents=matching_docs, question=prompt)
        st.write('Query Result:')
        st.write(answer)


if selected_feature == "Upload & Analyze Custom Document":
    # Create a Streamlit file uploader widget
    uploaded_file = st.file_uploader(
        "Upload a PDF, DOCX, or TXT file", type=["pdf", "docx", "txt"])

    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Load the document
        documents = load_single_doc(uploaded_file)

        # store the split documnets in docs variable
        docs = split_docs(documents)

        # store the embeddings in db variable
        db = store_embeddings_in_chromadb(docs)

        
        #input prompt
        prompt = st.chat_input("Query your file")

        #display results
        retrieve_and_answer_question(prompt)

        

elif selected_feature == "Query Existing Documents":
    pass
