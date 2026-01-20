from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.chain_service import get_general_chain
from app.services.vectordb_service import ingest_items, search, ingest_text

router = APIRouter(
    prefix="/vector-ops",
    tags=["vector-ops"]
)

# A quick Pydantic model for document ingestion
class IngestItem(BaseModel):
    id: str
    text:str
    metadata: dict[str, Any] | None = None

# Another quick model for ingesting raw text
class IngestTextRequest(BaseModel):
    text: str

# Another quick model for similarity search request results
class SearchRequest(BaseModel):
    query: str = ""
    k:int = 3

# Importing the basic chain for use in the LLM-powered endpoints
chain = get_general_chain()

# Endpoint for data ingestion
@router.post("/ingest-json")
async def ingest_json(items:list[IngestItem]):

    # Call the service method to ingest items
    count = ingest_items([item.model_dump() for item in items])
    return {"ingested:":count}

# Endpoint for similarity search
@router.post("/search-items")
async def items_similarity_search(request:SearchRequest):
    return search(request.query, request.k)

# Endpoint for raw text ingestion
@router.post("/ingest-text")
async def ingest_raw_text(request:IngestTextRequest):
    count = ingest_text(request.text)
    return {"ingested chunks: ":count}

# Endpoint with LLM-powered response that uses the boss_plans collection
@router.post("/search-plans")
async def search_plans(request:SearchRequest):
    result = search(request.query, request.k, collection="boss_plans")

    # Really quick prompt that tells the LLM the returned results
    # and asks for it to answer the user based on those results
    prompt = (
        f"Based on the following extracted info from a boss's evil plans,"
        f"Answer the user's query to the best of your ability."
        f"If there's no relevant information stored, you can say that."
        f"Extracted info: {result}"
        f"User query: {request.query}"
    )

    # Invoke our general chain from chain_service
    return chain.invoke({"input":prompt})
