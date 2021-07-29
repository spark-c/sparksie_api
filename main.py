
from fastapi import FastAPI
import ezgmail
import os
import json
from typing import Union, List, Dict


ezgmail.init()

app: FastAPI = FastAPI()

@app.get("/")
async def root() -> Dict[str,str]:
    return {"hello": "world"}

@app.get("/send_email")
async def send_email() -> Dict[str, str]:
    
    return {"key": "value"}