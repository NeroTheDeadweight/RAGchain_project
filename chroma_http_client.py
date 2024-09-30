from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
import chromadb
import jsonlines
import os
from langchain import hub
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document




def make_set(jsonl_dataset):
    with jsonlines.open(jsonl_dataset) as reader:
        ist = [obj['question'] + ' ' + obj['answer'] for obj in reader]
    return ist


def make_document(set):
    text = make_set(set)
    doc = []
    for elements in text:
        doc.append(Document(elements))
    return doc


def make_db(doc):
    chroma_client = chromadb.HttpClient(
        host="localhost",
        port=8000,
        ssl=False,
        headers=None,
        settings=Settings()
    )
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    collection = chroma_client.get_or_create_collection(name="vectorstore")
    vectorstore_from_http = Chroma(client=chroma_client, collection_name="vectorstore",
                                   embedding_function=embeddings)
    vectorstore_from_http.add_documents(documents=doc)
    retriever = vectorstore_from_http.as_retriever(search_type="similarity", search_kwargs={"k": 1})
    return retriever


