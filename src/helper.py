from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
#Extraer el texto de los pdfs
def load_pdf_file(data):
    loader = DirectoryLoader(   
        data,
        glob="**/*.pdf", 
        loader_cls=PyPDFLoader
        )
    documents = loader.load()
    return documents

from typing import List
from langchain_core.documents import Document

def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    minimal_docs: List[Document] = []
    for doc in docs:
        src = doc.metadata.get("source")
        minimal_docs.append(
            Document(
                page_content=doc.page_content, 
                metadata={"source": src}
                )
            )
    return minimal_docs

#Separar el documento principal pdf en varios trzos
def text_split(minimal_docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20
    )
    texts_chunk = text_splitter.split_documents(minimal_docs)
    return texts_chunk

#Embedding model
from langchain_huggingface import HuggingFaceEmbeddings

def download_hugging_face_embeddings():
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
    )
    return embeddings

