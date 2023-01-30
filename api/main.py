import os
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Dict, List, Any
from pydantic import BaseModel

import smtplib
import ssl
from email.message import EmailMessage
from tempfile import NamedTemporaryFile

from kidslinkedConverter import kidslinkedConverter as kc




### Init ###

app: FastAPI = FastAPI()
origins: List[str] = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost",
    "http://localhost:8000",
    "https://spark-c.github.io"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

smtp_port: int = 465
smtp_password: str = os.environ["PASSWORD"]


### Endpoints ###

@app.get("/")
async def root() -> Dict[str,str]:
    return {"hello": "world"}

# email #

class Email(BaseModel):
    sender_name: str
    sender_email: str
    subject: str
    body: str


@app.post("/send_email")
async def send_email(email: Email) -> Dict[str, str]:
    if email:
        target_email: str = "cklsparks@gmail.com"

        mail: EmailMessage = EmailMessage()
        mail.set_content(email.body)
        mail["Subject"] = email.subject
        mail["To"] = target_email
        mail["From"] = "sparksie.api@gmail.com"
        mail["Cc"] = email.sender_email

        try:
            context: ssl.SSLContext = ssl.create_default_context()
            with smtplib.SMTP_SSL(
                    "smtp.gmail.com",
                    smtp_port,
                    context=context
                ) as server: 

                server.login("sparksie.api@gmail.com", smtp_password)
                server.send_message(mail)

        except Exception as e:
            print(f"Something went wrong sending!\n{e}")
            # TODO send error code
            return {"placeholder": "couldn't send"}
    else:
        # TODO error code
        return {"placeholder": "missing parameters"}

    return {"placeholder": "success 200"}


# converter #

class ContactData(BaseModel):
    raw: str

class ParsedData(BaseModel):
    data: List[Dict[str, Any]]

@app.post("/kc_parse")
async def kc_parse(contact_data: ContactData) -> Dict[str,int|List[Dict[str, Any]]]:
    parsed: List[Dict[str, str]] = kc.compile_for_remote({'message': contact_data.raw})
    return {
        "count": len(parsed),
        "data": parsed
    }


@app.post("/kc_get_workbook")
async def kc_get_workbook(parsed_data: ParsedData) -> Any:
    wb: Any = kc.generate_wb(parsed_data.data)
    with NamedTemporaryFile() as tmp:
        wb.save(tmp.name)
        tmp.seek(0)
        stream = tmp.read()
    return Response(content=stream, media_type="application/ms-excel")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)