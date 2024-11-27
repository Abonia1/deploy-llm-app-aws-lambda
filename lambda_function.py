import boto3
import bs4
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

# change it in env variable
# configuration > Environment variables > OPENAI_API_KEY
OPENAI_API_KEY =  os.environ['OPENAI_API_KEY']
print(OPENAI_API_KEY)

# load the data from web
def load_data():
    # Load, chunk and index the contents of the blog.
    loader = WebBaseLoader(
        web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                class_=("post-content", "post-title", "post-header")
            )
        ),
    )
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
    # Retrieve and generate using the relevant snippets of the blog.
    retriever = vectorstore.as_retriever()
    return retriever
    
def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

def get_response(query):
    prompt = hub.pull("rlm/rag-prompt")
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    retriever = load_data()
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain.invoke(query)


def lambda_handler(event, context):
    query = event.get("question")
    

    response = get_response(query)
    print("response:", response)
    return {"body": response, "statusCode": 200}
