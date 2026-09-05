"""
main.py - FastAPI app for HR Assistant RAG Chatbot
"""

import os
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from config import UPLOAD_FOLDER, INDEX_STORE
from rag.vectorstore import allowed_file, add_file_to_index, delete_file_from_index, vectorstore
from rag.pipeline import rag_search

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(INDEX_STORE, exist_ok=True)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup_load():
    """Index any existing files in UPLOAD_FOLDER not yet in the vectorstore."""
    existing = vectorstore.get()
    indexed_files = {m["filename"] for m in existing["metadatas"]} if existing["metadatas"] else set()
    for fname in os.listdir(UPLOAD_FOLDER):
        if fname.endswith(".txt") and fname not in indexed_files:
            with open(os.path.join(UPLOAD_FOLDER, fname), "r", encoding="utf-8") as f:
                add_file_to_index(fname, f.read())


# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/manage", response_class=HTMLResponse)
async def manage(request: Request):
    return templates.TemplateResponse(request, "manage.html")


@app.get("/list_files")
async def list_files():
    files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".txt")]
    return {"files": files}


@app.post("/upload")
async def upload_files(request: Request, files: list[UploadFile] = File(..., alias="files[]")):
    uploaded = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = os.path.basename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            content = await file.read()
            with open(filepath, "wb") as f:
                f.write(content)
            add_file_to_index(filename, content.decode("utf-8"))
            uploaded.append(filename)
    return {"uploaded": uploaded, "message": f"Uploaded {len(uploaded)} files. Index updated."}


@app.post("/delete_file")
async def delete_file(request: Request):
    data = await request.json()
    filename = data.get("filename")
    path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(path):
        return JSONResponse({"error": "File not found"}, status_code=404)
    os.remove(path)
    delete_file_from_index(filename)
    return {"deleted": filename, "message": "File deleted and index updated."}


@app.post("/search")
async def search(request: Request):
    data = await request.json()
    query = data.get("query", "")
    k = int(data.get("top_k", 3))
    history = data.get("history", [])

    resp, code = rag_search(query, k, history)

    return JSONResponse(resp, status_code=code)


# -----------------------------------------------------------------------------
# Main Entrypoint
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    import webbrowser
    import threading

    def open_browser():
        webbrowser.open("http://localhost:8000")

    threading.Timer(1.5, open_browser).start()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
