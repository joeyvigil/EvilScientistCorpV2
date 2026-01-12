# This service module will store logic that returns chains
# a chain in LangChain is just a sequence of actions/info that we send to an LLM
# all in the hopes of getting an appropriate response
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

# Define the LLM we're going to use
llm = ChatOllama(
    model="llama3.2:3b", # The model we're using (we installed llama3.2:3b)
    temperature=0.2 # Temp goes from 0-1. Higher temp = more creativity
)

# Define the general prompt we'll send to the LLM (helps with tone and context)
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful chatbot that assists with queries in the fictional Evil Scientist Corporation. "
               "You help the scientists with their evil schemes, and you are pretty evil yourself. "
               "Your tone is conniving and blunt, with a focus on problem solving and efficiency. "
               "You don't provide further suggestions beyond what is asked. Keep your answers concise."),
    ("user", "{input}")
])

# Basic general chain here
def get_general_chain():
    
    # This basic chain is just:
        # The llm we're talking to
        # The prompt we're sending to the llm
        # We defined both of these above!!
    chain = llm | prompt

    return chain

# More sequential chain that refines the answer more


# A chain that focuses only on math operations
