import sys
import os
from fastapi.staticfiles import StaticFiles

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from main import rag_chain

app = FastAPI(title="langchain", description="IA")

assets_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "front-end",
        "assets"
    )
)

app.mount(
    "/assets",
    StaticFiles(directory=assets_path),
    name="assets"
)

app.mount(
    "/assets",
    StaticFiles(directory=assets_path),
    name="assets"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_routes(app, rag_chain, path="/rag")


@app.get("/", response_class=HTMLResponse)
def get_chat_page():
    html_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "front-end", "index.html")
    )
    
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='localhost', port=8000)