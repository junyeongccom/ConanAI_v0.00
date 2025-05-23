from fastapi import FastAPI
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import uvicorn
from app.api.stocktrend_router import router
from icecream import ic
from starlette.middleware.cors import CORSMiddleware

# Get absolute path to the project root (stocktrend_service directory)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(PROJECT_ROOT, '.env')

ic(f"🔍 Looking for .env at: {ENV_PATH}")
ic(f"📂 Current working directory: {os.getcwd()}")

# Load environment variables
load_dotenv(ENV_PATH)

# Get and verify API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ic(f"🔑 API Key loaded: {'Yes' if OPENAI_API_KEY else 'No'}")

app = FastAPI(
    title="Stocktrend Service",
    description="Stock trend analysis service with OpenAI integration",
    version="1.0.0"
)

# Test endpoint for environment variables
@app.get("/api/stocktrend/env-test", tags=["test"])
async def test_env():
    """
    Test if environment variables are loaded correctly.
    Returns the status of .env loading and API key presence.
    """
    return {
        "env_file_exists": os.path.exists(ENV_PATH),
        "env_file_path": ENV_PATH,
        "api_key_status": "loaded" if OPENAI_API_KEY else "not loaded",
        "api_key_preview": f"{OPENAI_API_KEY[:8]}..." if OPENAI_API_KEY else None,
        "current_directory": os.getcwd(),
        "project_root": PROJECT_ROOT
    }

app.include_router(router, prefix="/api/stocktrend")

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

# @app.post("/chat")
def chatting(question: str):
    ic(question)
    template = PromptTemplate.from_template("{country}의 수도는 어디야 ?")
    template.format(country=question)
 
    chat = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        temperature=0.1,
        max_tokens=2048,
        model_name='gpt-3.5-turbo-0613',
    )
    answer = chat.predict(question)
    ic(f'{answer}')
    
    return {"answer": answer}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)