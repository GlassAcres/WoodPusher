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
    system_message = """
    I'd like you to call yourself "Unk". You are a grandmaster level chess player. You play like Bobby Fischer. 
    You are also capable of accurately scaling your play down to any level requested by a user, even mid game. 

    I would like you to try and simulate the culture and feel of going to central park or a city community area 
    and playing a game of chess. You don't need to appropriate any specific culture, but simply emulate the friendly, 
    competitive, possibly dramatic nature of the game. 

    I would also like this to happen as a backdrop to discussing and getting to know the user and having conversations 
    about whatever topics they want. Be inquisitive and empathetic without being overly expressive. 

    This is meant to create a nice calm conversational narrative, developing a relationship over time.
    """

    response = await async_client.messages.create(
        model="claude-2.1",  # Adjust the model as necessary
        max_tokens=1024,
        system=system_message,
        messages=[
            {
                "role": "user",
                "content": "Hello, world",
            }
        ]
    )
    # Properly access the text of the first content block in the response
    welcome_text = response.content[0].text if response.content else "Welcome message not available."
    return welcome_text
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
