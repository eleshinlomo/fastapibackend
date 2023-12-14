# uvicorn main:app
# uvicorn main:app --reload

# Main imports
import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import openai
import traceback


load_dotenv()


# Custom function imports
from functions.text_to_speech import convert_text_to_speech
from functions.openai_requests import convert_audio_to_text, get_chat_response
from functions.database import store_messages, reset_messages
from tempfile import NamedTemporaryFile


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
]


# CORS - Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
# Post bot response
# Note: Not playing back in browser when using post request.
@app.post("/post-audio")
async def post_audio(file: UploadFile = File(...)):
    try:
        print(file.filename)
        print("Received audio file")

        with open('./file', 'wb') as buffer:
            buffer.write(file.file.read())
        audio_file = open(file.filename, 'rb')

        print("Decoding audio...")
        # Decode audio
        message_decoded = convert_audio_to_text(audio_file)
        print("Decoding complete")

        # Guard: Ensure output
        if not message_decoded:
            raise HTTPException(status_code=400, detail="Failed to decode audio")

        print("Getting chat response...")
        # Get chat response
        chat_response = get_chat_response(message_decoded)

        print("Chat response received")

        # Store messages
        store_messages(message_decoded, chat_response)

        # Guard: Ensure output
        if not chat_response:
            raise HTTPException(status_code=400, detail="Failed chat response")

        # Convert chat response to audio
        audio_output = convert_text_to_speech(chat_response)

        print("Audio conversion complete")

        # Guard: Ensure output
        if not audio_output:
            raise HTTPException(status_code=400, detail="Failed audio output")

        # Create a generator that yields chunks of data
        def iterfile():
            yield audio_output

        print("Returning response")
        # Return the user's audio response as a streaming response
        return StreamingResponse(iterfile(), media_type="application/octet-stream")

    except Exception as e:
        # Log the exception traceback
        traceback_str = traceback.format_exc()
        print(traceback_str)

        # Return the full traceback in the response
        return {"error": traceback_str}


