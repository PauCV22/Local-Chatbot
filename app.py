from flask import Flask, jsonify, request, render_template
from src.helper import load_pdf_file, filter_to_minimal_docs, text_split, download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from src.prompt import *
import os

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

embedding = download_hugging_face_embeddings()

index_name = "mathbot"
docsearch = PineconeVectorStore.from_existing_index(
    embedding=embedding,
    index_name="mathbot"
)

retriever = docsearch.as_retriever(search_type="similarity",search_kwargs={"k": 3})

chatmodel = ChatOllama(model="llama3.1", temperature=0)
prompt=ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt), 
        ("human", "{input}")
    ]
)

question_answer_chain = create_stuff_documents_chain(chatmodel, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    msg = request.form['msg']
    input = msg
    print(input)
    response = rag_chain.invoke({"input": msg})
    print("response :", response["answer"])
    return str(response["answer"])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
