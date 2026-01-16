from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.vectordb_service import ingest_items

router = APIRouter(
    prefix="/vector-ops",
    tags=["vector-ops"]
)

# A quick Pydantic model for document ingestion
class IngestItem(BaseModel):
    id: str
    text:str
    metadata: dict[str, Any] | None = None

# Another quick model for similarity search request results


# Endpoint for data ingestion
@router.post("/ingest")
async def ingest(items:list[IngestItem]):

    # Call the service method to ingest items
    count = ingest_items([item.model_dump() for item in items])
    return {"ingested:":count}


# Endpoint for similarity search