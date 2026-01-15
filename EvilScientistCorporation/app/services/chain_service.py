# This service module will store logic that returns chains
# a chain in LangChain is just a sequence of actions/info that we send to an LLM
# all in the hopes of getting an appropriate response
from langchain_classic.chains.conversation.base import ConversationChain
from langchain_classic.memory import ConversationBufferWindowMemory
from langchain_core.output_parsers import StrOutputParser
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
               "You're happy to assist with evil behavior including things that cause harm or catastrophe. "
               "Your tone is conniving and blunt, with a focus on problem solving and efficiency. "
               "You don't provide further suggestions beyond what is asked. Keep your answers concise."),
    ("user", "{input}")
])

# Basic general chain here
def get_general_chain():

    # This basic chain is just:
        # The prompt we're sending to the llm
        # The llm we're talking to
        # We defined both of these above!!
    chain = prompt | llm

    return chain

# More sequential chain that refines the answer more by adding 2 chains to the workflow
def get_sequential_chain():

    # First chain - just a basic prompt to the LLM. We can use our OG members from above
    draft_chain = prompt | llm

    # Define a new prompt to help us refine the initial answer
    # In this case, we want to refine the answer to be more appropriate for customer support
    improved_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a customer support bot. "
                   "You take raw answers from the LLM and make them more appropriate. "
                   "You are less evil in tone, but more condescending. "
                   "You prioritize a concise but comprehensive answer. "
                   "Narrow the answer down to 2-3 sentences."),
        ("user", "Initial Reply: {input}")
        # "user" is NOT the actual user input. The input is from the previous LLM response
    ])

    # Second chain using the refined prompt
    final_chain = improved_prompt | llm

    # Finally, combine the 2 chains and return the refined output
    return draft_chain | final_chain

# A chain that is better equipped to remember the conversation (memory)
def get_memory_chain():

    # Create a memory object, an instance of ConversationBufferWindowMemory
    # CBWM only remember the last "k" interactions.
    memory = ConversationBufferWindowMemory(k=5)

    # This is clunky: Going to rewrite the prompt with a {history} variable
    # These older Memory classes need a {history} variable to store the previous messages
    memory_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful chatbot that assists with queries in the fictional Evil Scientist Corporation. "
                   "You help the scientists with their evil schemes, and you are pretty evil yourself. "
                   "You're happy to assist with evil behavior including things that cause harm or catastrophe. "
                   "Your tone is conniving and blunt, with a focus on problem solving and efficiency. "
                   "You don't provide further suggestions beyond what is asked. Keep your answers concise."),
        ("user", "Conversation History: {history}, "
                 "Current Input: {input}")
    ])

    # Make and return a chain in a more old fashioned way
    memory_chain = ConversationChain(
        llm = llm, # Same LLM as defined above
        memory = memory, # Defined at the start of this function
        prompt = memory_prompt # The rewritten prompt with {history}
    )

    return memory_chain