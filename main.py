from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI(title="My First FASTAPI")

@app.get("/hello/{name}")
def say_hello(name:str):
    return { "greeting":f"Hello {name}" }