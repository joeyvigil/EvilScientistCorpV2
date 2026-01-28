# Evil Scientist Corporation v2
Evil Scientist V2 is an app uses FastAPI and ollama AI model to create an evil scientist character that can answer questions and provide information in a humorous and villainous manner.

## Run instructions
1. Clone the repository:
   ```bash
   git clone
    ```

2. Install ollama AI model by following the instructions at [Ollama's official website](https://ollama.com/).  
    ```make sure its running before starting the app```  

4. Install the required dependencies:
   ```bash
    pip install fastapi
    pip install uvicorn
    pip install langchain 
    pip install langchain-community 
    pip install langchain-ollama
    ollama pull llama3.2:3b
    pip install chromadb langchain-chroma 
    pip install spacy 
    python -m spacy download en_core_web_sm
    ollama pull nomic-embed-text 
    ```
    more dependencies may be required based on your environment.
    ```bash
    pip install sqlalchemy
    ```

5. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
    ```