from fastapi import APIRouter
from langchain_community.document_loaders import TextLoader
from pydantic import BaseModel

from app.services.chain_service import get_general_chain

#Typical Router setup
router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

# I'm going to make a model right here - we don't need to import it around
# So I'll skip making a dedicated model.py file
class ChatInputModel(BaseModel):
    input:str

# Import the chain-creation functions from the chain service here
general_chain = get_general_chain()

# Generic chatbot-esque endpoint
@router.post("/")
async def general_chat(chat:ChatInputModel):
    return general_chain.invoke(input={"input":chat.input})

# Endpoint that summarizes a .txt file
@router.get("/plan-summary")
async def summarize_plans():

    # Load in .txt file
    loader = TextLoader("app/files_to_load/boss_plans.txt")
    docs = loader.load() # return a list of langchain Document objects

    # Extract the text from the docs variable
    evil_plans_text = docs[0].page_content

    # Invoke the LLM and give it another small prompt to summarize the boss's plans
    return general_chain.invoke(
        {
            "input": f"Concisely summarize the following text from my boss: "
            f"{evil_plans_text}"
        }
    )

