# uvicorn main:app
# uvicorn main:app --reload
# Main imports
import os
import requests
from io import BytesIO
import uvicorn
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import StreamingResponse, FileResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from langchain.llms import openai
import traceback
import logging
from pydantic import BaseModel


load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Auth Functions
from auth import login_checker


# Media function imports
from functions.google_text_to_speech import google_text_to_speech_converter
from functions.openai_requests import get_chat_response
from functions.elevenlabs_transcriber import elevenlabs_transcribe
from functions.database import store_messages, reset_messages
from functions.whisper_speech_to_text import convert_audio_to_text
from functions.openai_text_to_speech import openai_text_to_speech_converter


# Get Environment Vars
openai.organization = os.environ.get("OPEN_AI_ORG")
openai.api_key = os.environ.get("OPENAI_API_KEY")


# Initiate App
app = FastAPI()


# CORS - Origins
origins = [
    "https://myafros.com",
    "https://crm.myafros.com",
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:3000",
    "http://localhost:3001",
]


# CORS - Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "The server is running fine"}

# Check health
@app.get("/health")
async def check_health():
    return {"response": "healthy"}


# Reset Conversation
@app.get("/reset")
async def reset_conversation():
    reset_messages()
    return {"response": "conversation reset"}






@app.post("/api/pdftoword")
async def post_audio(pdf_file: UploadFile = File(...)):
    try:
        # Save the file temporarily
        with open(pdf_file.filename, 'wb') as pdf_file_path:
            pdf_file_path.write(await pdf_file.file.read())
        
        # Open the saved PDF file for conversion
        pdf = open(pdf_file.filename, 'rb')
        converted_word_content = convert_pdf_to_docx(pdf)

        if converted_word_content:
            # Return the Word document content as a StreamingResponse
            return StreamingResponse(BytesIO(converted_word_content),
                                     media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                     headers={"Content-Disposition": "attachment; filename=output.docx"})
        else:
            raise HTTPException(status_code=500, detail="Error converting PDF to Word.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

        


# Voice to Voice API
@app.post("/api/post-audio")
async def post_audio(file: UploadFile = File(...)):

    try:    
        # Convert audio to text - production
        # Save the file temporarily
        
        with open(file.filename, 'wb') as audio_path:
             audio_path.write(file.file.read())

        audio_input = open(file.filename, 'rb')

             
             
        print(audio_input.name)
        text = convert_audio_to_text(audio_input)
        print({"decoded_message": text})
        # Guard: Ensure output
        if not text:
            raise HTTPException(status_code=400, detail="Failed to decode audio")
        
        # Send to model and get back chat response
        chat_response = get_chat_response(text)

        # Guard: Ensure output
        if not chat_response:
            raise HTTPException(status_code=400, detail="Failed chat response")

        # Convert chat response to audio
        # audio_output = openai_text_to_speech_converter(text, model='tts-1', voice='alloy')
        audio_output = google_text_to_speech_converter(chat_response)
        # Guard: Ensure output
        if not audio_output:
            raise HTTPException(status_code=400, detail="Failed audio output")


       # Return the user's audio response as a streaming response
        return FileResponse(audio_output, media_type="audio/mpeg", filename="output.mp3")

    except Exception as e:
        # Log the exception traceback
        traceback_str = traceback.format_exc()
        logger.error(traceback_str)

        # Return the full traceback in the response
        return {"error": traceback_str}
    






# Voice to Text api
@app.post('/api/voicetotext')
def transcribe_audio(audiofile: UploadFile = File(...)):
    try:
        # Save the file temporarily
        
        with open(audiofile.filename, 'wb') as audio_path:
            audio_path.write(audiofile.file.read())
        
        audio_data = open(audiofile.filename, 'rb')

        # Transcribe the audio
        transcribed_text = convert_audio_to_text(audio_data)

        print({"decoded_message": transcribed_text})

        # Guard: Ensure output
        if not transcribed_text:
            raise HTTPException(status_code=400, detail="Failed to decode audio")
        else:
            return {"data": transcribed_text, "ok": True}
    except Exception as e:
        return {"error": str(e), "ok": False}
    

    
# Text to Voice API
@app.post('/api/texttovoice')
async def convert_text_to_audio(request: Request):

    payload = await request.json()
    text = payload.get('text_message')
    
    try:

        # Convert text to audio
        if text:
            print({"Your text": text})
            audio = google_text_to_speech_converter(text)

            # Guard: Ensure output
            if not audio:
                raise Exception("Failed to decode audio")
            else:
               # Return the user's audio response as a streaming response
                return FileResponse(audio, media_type="audio/mpeg", filename="output.mp3")
        else:
            raise Exception("Text not found")
    except Exception as e:
        return {"error": str(e), "ok": False}
    




    