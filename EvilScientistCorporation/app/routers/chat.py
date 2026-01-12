from fastapi import APIRouter

from app.services.chain_service import get_general_chain

#Typical Router setup
router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

# I'm going to make a model right here - we don't need to import it around
# So I'll skip making a dedicated model.py file
class ChatInputModel:
    input:str

# Import the chain-creation functions from the chain service here
general_chain = get_general_chain()

# Generic chatbot-esque endpoint
@router.post("/")
async def general_chat(chat:ChatInputModel):
    return general_chain.invoke({"input":chat.input})