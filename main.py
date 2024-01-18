# uvicorn main:app
# uvicorn main:app --reload

# Main imports
import os
import io
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import openai
import traceback
import logging


load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Custom function imports
from functions.google_text_to_speech import text_to_speech
from functions.openai_requests import get_chat_response
from functions.elevenlabs_transcriber import elevenlabs_transcribe
from functions.database import store_messages, reset_messages
from functions.whisper_speech_to_text import convert_audio_to_text


# Get Environment Vars
openai.organization = os.environ.get("OPEN_AI_ORG")
openai.api_key = os.environ.get("OPEN_AI_KEY")


# Initiate App
app = FastAPI()


# CORS - Origins
origins = [
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


# Post bot response
# Note: Not playing back in browser when using post request.
@app.post("/api/post-audio")
async def post_audio(file: UploadFile = File(...)):

    try:    
        # Convert audio to text - production
        # Save the file temporarily
        
        with open(file.filename, 'wb') as audio_path:
             audio_path.write(file.file.read())

        audio_input = open(file.filename, 'rb')

             
             
        print(audio_input.name)
        message_decoded = convert_audio_to_text(audio_input)
        print({"decoded_message": message_decoded})
        # Guard: Ensure output
        if not message_decoded:
            raise HTTPException(status_code=400, detail="Failed to decode audio")

        # Get chat response
        chat_response = get_chat_response(message_decoded)

        # Store messages
        store_messages(message_decoded, chat_response)

        # Guard: Ensure output
        if not chat_response:
            raise HTTPException(status_code=400, detail="Failed chat response")

        # Convert chat response to audio
        audio_output = text_to_speech(chat_response)

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
    






# Transcriber api
@app.post('/api/transcriber')
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
            return transcribed_text
    except Exception as e:
        return str(e)




    