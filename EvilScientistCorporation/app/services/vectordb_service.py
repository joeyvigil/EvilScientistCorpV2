# This service will help us initialize and interact with a ChromaDB vector database
from typing import Any

from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.documents import Document

PERSIST_DIRECTORY = "app/chroma_store" # Where the DB will be stored on disk
COLLECTION = "evil_items" # What kind of data we're storing (like the tables in SQL)

# The actual chroma vector store itself
# This will be the chroma instance OR no value at all
vector_store: Chroma | None = None

# Initialize the ChromaDB vector store
def init_vector_store():
    # Use the global instance defined above to accomplish Singleton behavior
    global vector_store

    if vector_store is None:
        vector_store = Chroma(
            collection_name=COLLECTION,
            persist_directory=PERSIST_DIRECTORY,
            embedding_function=OllamaEmbeddings(model="nomic-embed-text")
        )

# Get an instance of the Chroma vector store (lets us interact with the DB instance)
def get_vector_store() -> Chroma:
    # We could raise an Exception here if vector_store is None
    return vector_store


# Ingest documents into the vector store (this is where the embeddings happen)
def ingest_items(items: list[dict[str, Any]]) -> int:

    # Get an instance of the vector store
    db_instance = get_vector_store()

    # Turn the input into a list of documents to get inserted
    docs = [
        Document(page_content=item["text"], metadata=item.get("metadata", {}))
        for item in items
    ]
    # Also, attach IDs to the documents (also found in the sample data)
    ids = [item["id"] for item in items]

    # Add the documents, return the length of the ingested items
    db_instance.add_documents(docs, ids=ids)
    return len(items)

# Search the vector store for similar or relevant documents based on a query
def search(query: str, k: int = 3) -> list[dict[str,Any]]:

    # Get an instance of the vector store
    db_instance = get_vector_store()

    # Save the results of the similarity search
    results = db_instance.similarity_search(query, k=k)

    # Return the results as a list of dicts with the expected fields
    return [
        {
            "text": result.page_content,
            "metadata": result.metadata
        }
        for result in results
    ]
