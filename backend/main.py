from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
import os

from dotenv import load_dotenv
from groq import Groq
from elevenlabs.client import ElevenLabs
load_dotenv()
app = FastAPI()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
eleven_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class Message(BaseModel):
    message: str


# 1️⃣ Check server
@app.get("/")
def home():
    return {"message": "AI University Helpdesk Running"}


# 2️⃣ Text → Text chatbot
@app.post("/chat")
def chat(msg: Message):

    user_message = msg.message

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a multilingual university helpdesk assistant. Always reply in the same language as the user."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    reply = response.choices[0].message.content

    return {"reply": reply}




# 3️⃣ Voice → Text
@app.post("/speech-to-text")
async def speech_to_text(file: UploadFile):

    audio = await file.read()

    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio
    )

    return {"text": transcript.text}

from fastapi.responses import FileResponse
import requests

@app.post("/text-to-speech")
def text_to_speech(msg: Message):

    text = msg.message

    url = "https://api.elevenlabs.io/v1/text-to-speech/RBJqcVOuibR3moRoviiH"

    headers = {
        "xi-api-key": os.getenv("ELEVENLABS_API_KEY"),
        "Content-Type": "application/json"
    }

    data = {
    "text": text,
    "model_id": "eleven_flash_v2"
}

    response = requests.post(url, json=data, headers=headers)

    print("ElevenLabs status:", response.status_code)

    with open("speech.mp3", "wb") as f:
        f.write(response.content)

    return FileResponse(
    "speech.mp3",
    media_type="audio/mpeg",
    filename="speech.mp3"
)