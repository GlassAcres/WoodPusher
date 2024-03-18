from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from email_service import send_email
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/signup")
async def signup(email: str = Form(...)):
    subject = "Welcome to Claude Email Chatbot!"
    body = "Thank you for signing up. This is the first message from your AI agent."
    await send_email(subject, email, body)
    return {"message": "Welcome email sent!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))