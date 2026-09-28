import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from langserve import add_routes
from main import rag_chain
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="langchain", description="IA")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_routes(app, rag_chain, path='')


@app.get("", response_class=HTMLResponse)
def get_chat_page():
    with open(os.path.join(os.path.dirname(__file__), "index.html"), "r", encoding="utf-8") as f:
        return f.read()
    
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host='localhost', port=8000)

