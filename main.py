from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI(title="My First FASTAPI")
origins = [
    "http://localhost:5173",  # local React dev
    "https://blue-pond-0e0901c10.3.azurestaticapps.net",  # deployed React app
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from travelPlanner.routes import extract, chat_agent  # noqa: F401


@app.get("/hello/{name}")
def say_hello(name:str):
    return { "greeting":f"Hello {name}" }

@app.post("/api/bills/upload")
def upload_bills(file:UploadFile=File(...)):
    print(file)
    return {
        "success": True,
        "filename": file.filename,
        "content_type": file.content_type
    }