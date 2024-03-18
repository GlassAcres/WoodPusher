from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import os
from anthropic import AsyncAnthropic
from email_service import send_email  # Corrected import
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Initialize the AsyncAnthropic client with your API key
async_client = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

async def generate_welcome_message():
    # Your existing code for generate_welcome_message

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/signup")
async def signup(email: str = Form(...)):
    welcome_message = await generate_welcome_message()
    try:
        await send_email("Welcome to Our AI Email Chat Service!", email, welcome_message)
        logger.info("Welcome email sent successfully.")
        return {"message": "Welcome email sent!"}
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        raise HTTPException(status_code=500, detail="Error sending email")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
