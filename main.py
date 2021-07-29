import os

# Attempts to generate ezgmail credentials.json and token.json 
# from envvars if the files are not already present.
# Seems necessary for use without exposing credentials in repo
if not os.path.isfile("credentials.json"):
    credContents: str = os.environ["CREDENTIALS"]
    try:
        with open("credentials.json", "w") as f:
            f.write(credContents)
            print(credContents)
    except:
        print("couldn't create ./credentials.json!")

if not os.path.isfile("token.json"):
    tokenContents: str = os.environ["TOKEN"]
    try:
        with open("token.json", "w") as f:
            f.write(tokenContents)
    except:
        print("couldn't create ./token.json!")

from fastapi import FastAPI
import ezgmail
from typing import Dict
from pydantic import BaseModel


class Email(BaseModel):
    sender_name: str
    sender_email: str
    subject: str
    body: str


ezgmail.init()
app: FastAPI = FastAPI()

@app.get("/")
async def root() -> Dict[str,str]:
    return {"hello": "world"}

@app.post("/send_email")
async def send_email(email: Email) -> Dict[str, str]:
    if email:
        target_email: str = "sparksie.api@gmail.com"
        message_body: str = (
            "Sent by:\n" +
            f"{email.sender_name}\n" +
            f"{email.sender_email}\n\n" +
            email.body
        )

        try:
            ezgmail.send(
                target_email,
                email.subject,
                message_body)
        except:
            print("Something went wrong sending!")
            # send error code
            return {"placeholder": "couldn't send"}
    else:
        # send error code
        return {"placeholder": "missing parameters"}

    return {"placeholder": "success 200"}