from fastapi import FastAPI
import json
from typing import Union, List, Dict


app: FastAPI = FastAPI()


@app.get("/")
async def root() -> None:
    pass

@app.get("/send_email")
async def send_email() -> Dict[str, str]:
    
    return {"key": "value"}