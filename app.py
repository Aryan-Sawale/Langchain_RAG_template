import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import Docx2txtLoader
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    api_key=openai_api_key,
    model="gpt-4.1-mini",
    temperature=0,
)

embeddings = OpenAIEmbeddings(
    api_key=openai_api_key,
    model="text-embedding-3-small",
)

def load_documents_with_docx2txt(folder_path: str):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".docx"):
            file_path = os.path.join(folder_path, filename)
            loader = Docx2txtLoader(file_path)
            documents.extend(loader.load())
    return documents

def build_retriever(folder_path: str):
    documents = load_documents_with_docx2txt(folder_path)
    texts = [doc.page_content for doc in documents]

    vectorstore = Chroma.from_texts(texts=texts, embedding=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    return retriever

template = """
You are an expert SQL assistant. Based on the following retrieved document information, generate the SQL query to answer the user's question.

Database Information:
{context}

User Query: 
{query}

Your response should include:
1. Explanation of which tables to join and why.
2. The SQL query.

Response:
"""

prompt_template = PromptTemplate.from_template(template)

def process_docs(docs: list[Document]):
    return "\n\n".join(doc.page_content for doc in docs)

def get_rag_chain(folder_path: str):
    retriever = build_retriever(folder_path)
    RAG_chain = (
        {
            "context": retriever | process_docs,
            "query": RunnablePassthrough()
        }
        | prompt_template
        | llm
        | StrOutputParser()
    )
    return RAG_chain

def query_rag(question: str, folder_path: str = "data") -> str:
    rag_chain = get_rag_chain(folder_path)
    response = rag_chain.invoke(question)
    return response
