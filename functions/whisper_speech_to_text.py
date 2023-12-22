
import openai

import os
import openai
from dotenv import load_dotenv
from fastapi import HTTPException
from langchain.chat_models import ChatOpenAI
from pydub import AudioSegment



load_dotenv()


params = {
    "temperature": 0.7,
    "max_tokens": 20,
}



# Open AI - Whisper
# Convert audio to text
def convert_audio_to_text(audio_data):
  try:
    

    transcript = openai.Audio.transcribe(
      model="whisper-1",
      file=audio_data,
      params=params
      
      )
    
    
    
    message_text = transcript["text"]
    return message_text
  except Exception as e:
    return
