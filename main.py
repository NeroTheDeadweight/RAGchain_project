from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
import gradio as gr
from sqldb_int import save_todb, get_chat_history
import chroma_http_client
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import getpass
load_dotenv()
# os.environ["OPENAI_API_KEY"] = getpass.getpass()
dataset = '21.jsonl'
sqlite_database = "sqlite:///data.db"
engine = create_engine(sqlite_database, echo=True)
def new_db_file(set):
    documents = chroma_http_client.make_document(set)
    retriever = chroma_http_client.make_db(documents)
    return retriever

retriever = new_db_file(dataset)
llm = ChatOpenAI(model="gpt-3.5-turbo-0125", api_key=os.environ["OPENAI_API_KEY"])
prompt = hub.pull("rlm/rag-prompt")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
)

def get_chunk(message):
    answer = ""
    for chunk in rag_chain.stream(message):
        # print(chunk, end="", flush=True)
        answer = answer + chunk
    return answer

def yes_man(message, history):
    if message == "History":
        mess = ""
        for text in get_chat_history():
            print(text)
            mess = mess+", \n"+text
        return mess
    else:
        save_todb(message)
        answer = get_chunk(message)
        save_todb(answer)
        return answer

demo = gr.ChatInterface(
    yes_man,
    chatbot=gr.Chatbot(height=300),
    textbox=gr.Textbox(placeholder="Ask me a question", container=False, scale=7),
    title="RAG Bot",
    description="Ask RAGBot any question",
    theme="soft",
    examples=["History", "Am I cool?", "Are tomatoes vegetables?"],
    cache_examples=True,
    retry_btn=None,
    undo_btn="Delete Previous",
    clear_btn="Clear",
)
demo.launch()
