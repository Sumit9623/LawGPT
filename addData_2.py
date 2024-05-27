from langchain.vectorstores import Qdrant
from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain_community.embeddings import GPT4AllEmbeddings
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from PyPDF2 import PdfReader


import qdrant_client
import os
from langchain.text_splitter import CharacterTextSplitter


client = qdrant_client.QdrantClient(os.getenv("QDRANT_HOST"),api_key=os.getenv("QDRANT_API_KEY"))
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
# embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-3-small")
vectorstore = Qdrant(client=client,collection_name=os.getenv("QDRANT_COLLECTION_NAME"),embeddings=embeddings)

def get_chunks():
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=8000,
        chunk_overlap=200,
        length_function=len
    )
    with open("story.txt") as f:
        raw_text = f.read()
    chunks = text_splitter.split_text(raw_text)
    return chunks

vectorstore.add_texts(get_chunks())