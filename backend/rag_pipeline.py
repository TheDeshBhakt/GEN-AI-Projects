import os
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI  # Using OpenAI as an example
from langchain.prompts import PromptTemplate

# --- Configuration ---
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
SOURCE_FILE = os.path.join(DATA_DIR, "scraped_data.json")
VECTORSTORE_DIR = os.path.join(os.path.dirname(__file__), "vectorstore")

# --- RAG Pipeline Components ---

# 1. Document Loader
def load_documents():
    """Loads the scraped data from the JSON file."""
    if not os.path.exists(SOURCE_FILE):
        # In a real app, you might want to trigger the scraper here
        raise FileNotFoundError(f"Source data file not found: {SOURCE_FILE}. Please run the scraper first.")

    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Convert the JSON data into LangChain's Document format
    from langchain.docstore.document import Document
    documents = [Document(page_content=item['content'], metadata={'source': item['url']}) for item in data]
    return documents

# 2. Text Splitter
def split_documents(documents):
    """Splits the documents into smaller chunks."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_documents(documents)

# 3. Embedding Model
def get_embedding_model():
    """Initializes the sentence-transformer embedding model."""
    # This will download the model on first use.
    return SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# 4. Vector Store
def create_vector_store(chunks, embedding_model):
    """Creates and persists the ChromaDB vector store."""
    if not os.path.exists(VECTORSTORE_DIR):
        os.makedirs(VECTORSTORE_DIR)

    vector_store = Chroma.from_documents(
        chunks,
        embedding_model,
        persist_directory=VECTORSTORE_DIR
    )
    vector_store.persist()
    return vector_store

def load_vector_store(embedding_model):
    """Loads the existing vector store."""
    if not os.path.exists(VECTORSTORE_DIR):
        return None
    return Chroma(persist_directory=VECTORSTORE_DIR, embedding_function=embedding_model)

# 5. LLM and QA Chain
def get_qa_chain(vector_store_retriever):
    """Initializes the QA chain with a custom prompt and an LLM."""
    # IMPORTANT: This requires an OpenAI API key to be set in the environment.
    # The user should create a .env file in the 'backend' directory with:
    # OPENAI_API_KEY="your_openai_api_key"

    # Check for the API key
    if "OPENAI_API_KEY" not in os.environ:
        raise ValueError("OPENAI_API_KEY not found in environment variables. Please set it in a .env file.")

    llm = OpenAI(temperature=0.7)

    prompt_template = """
    You are an AI guide for the city of Varanasi. Use the following pieces of context to answer the user's question.
    If you don't know the answer from the context, just say that you don't have enough information, don't try to make up an answer.
    Provide a helpful and friendly answer.

    Context: {context}

    Question: {question}

    Answer:
    """

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store_retriever,
        chain_type_kwargs={"prompt": PROMPT},
        return_source_documents=True
    )
    return qa_chain

# --- Main Function to get an answer ---

def get_answer_from_query(query: str):
    """
    The main function that orchestrates the RAG pipeline to answer a query.
    """
    embedding_model = get_embedding_model()

    # Load or create the vector store
    vector_store = load_vector_store(embedding_model)
    if vector_store is None:
        print("Vector store not found. Creating a new one from source data...")
        documents = load_documents()
        chunks = split_documents(documents)
        vector_store = create_vector_store(chunks, embedding_model)
        print("Vector store created successfully.")

    # Create the QA chain
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    qa_chain = get_qa_chain(retriever)

    # Get the answer
    result = qa_chain({"query": query})

    # You can also include the source documents in the response if needed
    # sources = [doc.metadata['source'] for doc in result['source_documents']]

    return result['result']

# --- To test this module independently ---
if __name__ == "__main__":
    # This is an example of how to use the module.
    # Make sure you have a .env file with your OPENAI_API_KEY.
    # And make sure you have run the scraper.py first to generate the data.

    # Example query
    test_query = "What are some famous places to visit in Varanasi?"

    try:
        answer = get_answer_from_query(test_query)
        print(f"Query: {test_query}")
        print(f"Answer: {answer}")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
