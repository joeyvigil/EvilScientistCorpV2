from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from starlette.requests import Request
from starlette.responses import JSONResponse

from app.routers import users, items, chat, vector_ops
from app.services.vectordb_service import init_vector_store


# Setting up a context manager for lifespan events
# We'll use this to initialize our Chroma vector DB when the app starts
@asynccontextmanager
async def lifespan(app:FastAPI):
    # store the vector DB init in app state (a way to store global data in FastAPI)
    app.state.vector_store = init_vector_store()
    yield # pause here and run the app


# Set up FastAPI. We'll use this "app" variable to do FastAPI stuff below
app = FastAPI(lifespan=lifespan)

# Setting CORS (Cross Origin Resource Sharing) policy
# origins = ["*"] # Allow all origins (not recommended for production)
origins = ["http://localhost"] # Allows requests only from localhost

#TODO for Ben: CORS middleware setup

# Global custom Exception Handler
# All Exceptions raised in the routers get handled here
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request:Request, exception:HTTPException):
    return JSONResponse(
        status_code=exception.status_code,
        content={"message":exception.detail}
    )

# Import routers here
app.include_router(users.router)
app.include_router(items.router)
app.include_router(chat.router)
app.include_router(vector_ops.router)

# Generic sample endpoint (GET request that just returns a message)
@app.get("/")
async def sample_endpoint():
    return {"message":"Hello FastAPI!"}
