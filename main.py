from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from email_service import send_email
import os
from anthropic import AsyncAnthropic

app = FastAPI()
templates = Jinja2Templates(directory="templates")

async_client = AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

async def generate_welcome_message():
    message = await async_client.messages.create(
        max_tokens=1000,
        system: "Your name is Unk. You are a savy and charismatic friend who is meant to have daily chats with users, which playing chess."
        messages=[
            {"role": "user", "content": "Hello, world"}
        ],
        model="claude-3-opus-20240229",
    )
    return message.content[0].text

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/signup")
async def signup(email: str = Form(...)):
    welcome_message = await generate_welcome_message()
    await send_email("Welcome to Our AI Email Chat Service!", email, welcome_message)
    return {"message": "Welcome email sent!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
